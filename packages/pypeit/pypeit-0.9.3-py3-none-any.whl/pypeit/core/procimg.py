""" Module for image processing core methods
"""
from __future__ import (print_function, absolute_import, division, unicode_literals)

import astropy.stats
import numpy as np
from scipy import signal, ndimage
from pypeit import msgs
from pypeit import utils
from pypeit.core import parse


from pypeit import debugger


# TODO: Add sigdev to the high-level parameter set so that it can be
# changed by the user?
# JFH I think this crappy code below is deprecated
def find_bad_pixels(bias, numamplifiers, datasec, sigdev=10.0, trim=True):
    """
    Identify bad pixels in the datasection of the bias frame based on
    their robust deviation from the median.

    Args:
        bias (:obj:`numpy.ndarray`):
            Bias frame
        numamplifiers (int):
            Number of amplifiers
        datasec (list):
            List of slices, one per amplifier, that contain the data in
            the raw frame.  The slices and be lists of slice ojects or
            strings.  If they are strings, :func:`parse.sec2slice` is
            used to convert them for use in the function.
        sigdev (:obj:`float`, optional):
            Number of robust standard deviations beyond which to flag
            pixels as bad.
        trim (:obj:`bool`, optional):
            Flag to trim image to the data section.

    Returns:
        :obj:`numpy.ndarray`: An integer array with bad pixels set to 1.

    Raises:
        ValueError:
            Raised if the number of data sections does not match the
            number of amplifiers.
    """
    # Check input
    if len(datasec) != numamplifiers:
        raise ValueError('Number of amplifiers does not match provided data sections.')

    # If the input image sections are strings, convert them
    if isinstance(datasec[0], str):
        _datasec = datasec.copy()
        for i in range(numamplifiers):
            _datasec[i] = parse.sec2slice(datasec[i], require_dim=2)
    else:
        _datasec = datasec

    # Find the bad pixels and mask them
    mask = np.zeros_like(bias, dtype=np.int8)
    is_data = np.zeros_like(bias, dtype=bool)
    for i in range(numamplifiers):
        is_data[datasec[i]] = True
        temp = np.abs(np.median(bias[datasec[i]])-bias[datasec[i]])
        sigval = 1.4826*max(np.median(temp), 1)
        mask[datasec[i]][temp > sigdev*sigval] = 1

    msgs.info("Identified {0:d} bad pixels".format(int(np.sum(mask))))
    return trim_frame(mask, np.invert(is_data)) if trim else mask


#def badpix(frame, numamplifiers, datasec, sigdev=10.0):
#    """
#    frame is a master bias frame
#    numamplifiers : int
#    datasec : list
#    sigdev is the number of standard deviations away from the median that a pixel needs to be in order to be classified as a bad pixel
#    """
#    bpix = np.zeros_like(frame, dtype=np.int)
#    subfr, tframe, temp = None, None, None
#    #for i in range(settings.spect[dnum]['numamplifiers']):
#    for i in range(numamplifiers):
#        #datasec = "datasec{0:02d}".format(i+1)
#        x0, x1 = datasec[i][0][0], datasec[i][0][1]
#        y0, y1 = datasec[i][1][0], datasec[i][1][1]
#        #x0, x1 = settings.spect[dnum][datasec][0][0], settings.spect[dnum][datasec][0][1]
#        #y0, y1 = settings.spect[dnum][datasec][1][0], settings.spect[dnum][datasec][1][1]
#        xv = np.arange(x0, x1)
#        yv = np.arange(y0, y1)
#        # Construct an array with the rows and columns to be extracted
#        w = np.ix_(xv,yv)
#        tframe = frame[w]
#        temp = np.abs(np.median(tframe)-tframe)
#        sigval = max(np.median(temp)*1.4826, 1.4826)
#        ws = np.where(temp > sigdev*sigval)
#        subfr = np.zeros(tframe.shape, dtype=np.int)
#        subfr[ws] = 1
#        bpix[w] = subfr
#    del subfr, tframe, temp
#    # Finally, trim the bad pixel frame
#    bpix = trim(bpix, numamplifiers, datasec)
#    msgs.info("Identified {0:d} bad pixels".format(int(np.sum(bpix))))
#    return bpix


#def bias_subtract(rawframe, msbias, numamplifiers=None, datasec=None, oscansec=None):
#    """ Core routine for bias subtraction
#    Calls sub_overscan if msbias == 'overscan'
#
#    Parameters
#    ----------
#    rawframe : ndarray
#    msbias : ndarray or str
#
#    Returns
#    -------
#    newframe : ndarray
#      Bias subtracted frame
#
#    """
#    if isinstance(msbias, np.ndarray):
#        msgs.info("Subtracting bias image from raw frame")
#        # Subtract the master bias frame
#        return rawframe-msbias
#    elif isinstance(msbias, basestring) and msbias == 'overscan':
#        return subtract_overscan(rawframe, numamplifiers, datasec, oscansec, settings=None)
#    
#    msgs.error('Could not subtract bias level with the input bias approach.')


'''
def error_frame_postext(sciframe, idx, fitsdict, settings_spect):
    # Dark Current noise
    dnoise = settings.spect['det']['darkcurr'] * float(fitsdict["exptime"][idx])/3600.0
    # The effective read noise
    rnoise = settings.spect['det']['ronoise']**2 + (0.5*settings.spect['det']['gain'])**2
    errframe = np.zeros_like(sciframe)
    w = np.where(sciframe != -999999.9)
    errframe[w] = np.sqrt(sciframe[w] + rnoise + dnoise)
    w = np.where(sciframe == -999999.9)
    errframe[w] = 999999.9
    return errframe
'''

'''
def get_datasec_trimmed(spectrograph, scifile, det, settings_det,
                        naxis0=None, naxis1=None):
    """
    Primarily a wrapper with calls to get_datasec and pix_to_amp()

    Parameters
    ----------
    spectrograph : str
    scifile : str
    numamplifiers : int
    det : int
    settings_det : dict
    naxis0 : int, optional
    naxis1 : int, optional

    Returns
    -------
    datasec_img : ndarray
    naxis0 : int
    naxis1 : int
    """
    # Instrument specific bits
    # TODO -- Remove instrument specific items in a method like this
    if spectrograph in ['keck_lris_blue', 'keck_lris_red', 'keck_deimos']:
        # Grab
        datasec, oscansec, naxis0, naxis1 = get_datasec(spectrograph, scifile,
                                                        numamplifiers=settings_det['numamplifiers'], det=det)
        # Fill (for backwards compatability)
        for kk in range(settings_det['numamplifiers']):
            sdatasec = "datasec{0:02d}".format(kk+1)
            settings_det[sdatasec] = datasec[kk]
            soscansec = "oscansec{0:02d}".format(kk+1)
            settings_det[soscansec] = oscansec[kk]
        #fitstbl['naxis0'][scidx] = naxis0
        #fitstbl['naxis1'][scidx] = naxis1

    # Build the datasec lists for pix_to_amp
    datasec = []
    for i in range(settings_det['numamplifiers']):
        sdatasec = "datasec{0:02d}".format(i+1)
        datasec.append(settings_det[sdatasec])
    # Call
    #naxis0, naxis1 = int(fitstbl['naxis0'][scidx]), int(fitstbl['naxis1'][scidx])
    datasec_img = arpixels.pix_to_amp(naxis0, naxis1, datasec, settings_det['numamplifiers'])
    return datasec_img, naxis0, naxis1
'''


'''
def sn_frame(slf, sciframe, idx):
    # Dark Current noise
    dnoise = settings.spect['det']['darkcurr'] * float(slf._fitsdict["exptime"][idx])/3600.0
    # The effective read noise
    rnoise = np.sqrt(settings.spect['det']['ronoise']**2 + (0.5*settings.spect['det']['gain'])**2)
    errframe = np.abs(sciframe) + rnoise + dnoise
    # If there are negative pixels, mask them as bad pixels
    w = np.where(errframe <= 0.0)
    if w[0].size != 0:
        msgs.warn("The error frame is negative for {0:d} pixels".format(w[0].size)+msgs.newline()+"Are you sure the bias frame is correct?")
        msgs.info("Masking these {0:d} pixels".format(w[0].size))
        errframe[w]  = 0.0
        slf._bpix[w] = 1.0
    w = np.where(errframe > 0.0)
    snframe = np.zeros_like(sciframe)
    snframe[w] = sciframe[w]/np.sqrt(errframe[w])
    return snframe
'''


def lacosmic(det, sciframe, saturation, nonlinear, varframe=None, maxiter=1, grow=1.5,
             remove_compact_obj=True, sigclip=5.0, sigfrac=0.3, objlim=5.0):
    """
    Identify cosmic rays using the L.A.Cosmic algorithm
    U{http://www.astro.yale.edu/dokkum/lacosmic/}
    (article : U{http://arxiv.org/abs/astro-ph/0108003})
    This routine is mostly courtesy of Malte Tewes

    Args:
        det:
        sciframe:
        saturation:
        nonlinear:
        varframe:
        maxiter:
        grow:
        remove_compact_obj:
        sigclip:
        sigfrac:
        objlim:

    Returns:
        ndarray: mask of cosmic rays (0=no CR, 1=CR)

    """

    dnum = parse.get_dnum(det)

    msgs.info("Detecting cosmic rays with the L.A.Cosmic algorithm")
#    msgs.work("Include these parameters in the settings files to be adjusted by the user")
    # Set the settings
    scicopy = sciframe.copy()
    crmask = np.cast['bool'](np.zeros(sciframe.shape))
    sigcliplow = sigclip * sigfrac

    # Determine if there are saturated pixels
    satpix = np.zeros_like(sciframe)
#    satlev = settings_det['saturation']*settings_det['nonlinear']
    satlev = saturation*nonlinear
    wsat = np.where(sciframe >= satlev)
    if wsat[0].size == 0: satpix = None
    else:
        satpix[wsat] = 1.0
        satpix = np.cast['bool'](satpix)

    # Define the kernels
    laplkernel = np.array([[0.0, -1.0, 0.0], [-1.0, 4.0, -1.0], [0.0, -1.0, 0.0]])  # Laplacian kernal
    growkernel = np.ones((3,3))
    for i in range(1, maxiter+1):
        msgs.info("Convolving image with Laplacian kernel")
        # Subsample, convolve, clip negative values, and rebin to original size
        subsam = utils.subsample(scicopy)
        conved = signal.convolve2d(subsam, laplkernel, mode="same", boundary="symm")
        cliped = conved.clip(min=0.0)
        lplus = utils.rebin_evlist(cliped, np.array(cliped.shape)/2.0)

        msgs.info("Creating noise model")
        # Build a custom noise map, and compare  this to the laplacian
        m5 = ndimage.filters.median_filter(scicopy, size=5, mode='mirror')
        if varframe is None:
            noise = np.sqrt(np.abs(m5))
        else:
            noise = np.sqrt(varframe)
        msgs.info("Calculating Laplacian signal to noise ratio")

        # Laplacian S/N
        s = lplus / (2.0 * noise)  # Note that the 2.0 is from the 2x2 subsampling

        # Remove the large structures
        sp = s - ndimage.filters.median_filter(s, size=5, mode='mirror')

        msgs.info("Selecting candidate cosmic rays")
        # Candidate cosmic rays (this will include HII regions)
        candidates = sp > sigclip
        nbcandidates = np.sum(candidates)

        msgs.info("{0:5d} candidate pixels".format(nbcandidates))

        # At this stage we use the saturated stars to mask the candidates, if available :
        if satpix is not None:
            msgs.info("Masking saturated pixels")
            candidates = np.logical_and(np.logical_not(satpix), candidates)
            nbcandidates = np.sum(candidates)

            msgs.info("{0:5d} candidate pixels not part of saturated stars".format(nbcandidates))

        msgs.info("Building fine structure image")

        # We build the fine structure image :
        m3 = ndimage.filters.median_filter(scicopy, size=3, mode='mirror')
        m37 = ndimage.filters.median_filter(m3, size=7, mode='mirror')
        f = m3 - m37
        f /= noise
        f = f.clip(min=0.01)

        msgs.info("Removing suspected compact bright objects")

        # Now we have our better selection of cosmics :

        if remove_compact_obj:
            cosmics = np.logical_and(candidates, sp/f > objlim)
        else:
            cosmics = candidates
        nbcosmics = np.sum(cosmics)

        msgs.info("{0:5d} remaining candidate pixels".format(nbcosmics))

        # What follows is a special treatment for neighbors, with more relaxed constains.

        msgs.info("Finding neighboring pixels affected by cosmic rays")

        # We grow these cosmics a first time to determine the immediate neighborhod  :
        growcosmics = np.cast['bool'](signal.convolve2d(np.cast['float32'](cosmics), growkernel, mode="same", boundary="symm"))

        # From this grown set, we keep those that have sp > sigmalim
        # so obviously not requiring sp/f > objlim, otherwise it would be pointless
        growcosmics = np.logical_and(sp > sigclip, growcosmics)

        # Now we repeat this procedure, but lower the detection limit to sigmalimlow :

        finalsel = np.cast['bool'](signal.convolve2d(np.cast['float32'](growcosmics), growkernel, mode="same", boundary="symm"))
        finalsel = np.logical_and(sp > sigcliplow, finalsel)

        # Unmask saturated pixels:
        if satpix is not None:
            msgs.info("Masking saturated stars")
            finalsel = np.logical_and(np.logical_not(satpix), finalsel)

        ncrp = np.sum(finalsel)

        msgs.info("{0:5d} pixels detected as cosmics".format(ncrp))

        # We find how many cosmics are not yet known :
        newmask = np.logical_and(np.logical_not(crmask), finalsel)
        nnew = np.sum(newmask)

        # We update the mask with the cosmics we have found :
        crmask = np.logical_or(crmask, finalsel)

        msgs.info("Iteration {0:d} -- {1:d} pixels identified as cosmic rays ({2:d} new)".format(i, ncrp, nnew))
        if ncrp == 0: break
    # Additional algorithms (not traditionally implemented by LA cosmic) to remove some false positives.
    msgs.work("The following algorithm would be better on the rectified, tilts-corrected image")
    filt  = ndimage.sobel(sciframe, axis=1, mode='constant')
    filty = ndimage.sobel(filt/np.sqrt(np.abs(sciframe)), axis=0, mode='constant')
    filty[np.where(np.isnan(filty))]=0.0

    sigimg = cr_screen(filty)

    sigsmth = ndimage.filters.gaussian_filter(sigimg,1.5)
    sigsmth[np.where(np.isnan(sigsmth))]=0.0
    sigmask = np.cast['bool'](np.zeros(sciframe.shape))
    sigmask[np.where(sigsmth>sigclip)] = True
    crmask = np.logical_and(crmask, sigmask)
    msgs.info("Growing cosmic ray mask by 1 pixel")
    crmask = grow_masked(crmask.astype(np.float), grow, 1.0)

    return crmask.astype(bool)


def cr_screen(a, mask_value=0.0, spatial_axis=1):
    r"""
    Calculate the significance of pixel deviations from the median along
    the spatial direction.

    No type checking is performed of the input array; however, the
    function assumes floating point values.

    Args:
        a (numpy.ndarray): Input 2D array
        mask_value (float): (**Optional**) Values to ignore during the
            calculation of the median.  Default is 0.0.
        spatial_axis (int): (**Optional**) Axis along which to calculate
            the median.  Default is 1.

    Returns:
        numpy.ndarray: Returns a map of :math:`|\Delta_{i,j}|/\sigma_j`,
        where :math:`\Delta_{i,j}` is the difference between the pixel
        value and the median along axis :math:`i` and :math:`\sigma_j`
        is robustly determined using the median absolute deviation,
        :math:`sigma_j = 1.4826 MAD`.
    """
    # Check input
    if len(a.shape) != 2:
        msgs.error('Input array must be two-dimensional.')
    if spatial_axis not in [0,1]:
        msgs.error('Spatial axis must be 0 or 1.')

    # Mask the pixels equal to mask value: should use np.isclose()
    _a = np.ma.MaskedArray(a, mask=(a==mask_value))
    # Get the median along the spatial axis
    meda = np.ma.median(_a, axis=spatial_axis)
    # Get a robust measure of the standard deviation using the median
    # absolute deviation; 1.4826 factor is the ratio of sigma/MAD
    d = np.absolute(_a - meda[:,None])
    mada = 1.4826*np.ma.median(d, axis=spatial_axis)
    # Return the ratio of the difference to the standard deviation
    return np.ma.divide(d, mada[:,None]).filled(mask_value)


def grow_masked(img, grow, growval):

    if not np.any(img == growval):
        return img

    _img = img.copy()
    sz_x, sz_y = img.shape
    d = int(1+grow)
    rsqr = grow*grow

    # Grow any masked values by the specified amount
    for x in range(sz_x):
        for y in range(sz_y):
            if img[x,y] != growval:
                continue

            mnx = 0 if x-d < 0 else x-d
            mxx = x+d+1 if x+d+1 < sz_x else sz_x
            mny = 0 if y-d < 0 else y-d
            mxy = y+d+1 if y+d+1 < sz_y else sz_y

            for i in range(mnx,mxx):
                for j in range(mny, mxy):
                    if (i-x)*(i-x)+(j-y)*(j-y) <= rsqr:
                        _img[i,j] = growval
    return _img


def gain_frame(datasec_img, namp, gain_list):
    """ Generate a gain image

    Parameters
    ----------
    datasec_img : ndarray
    namp : int
    gain_list : list
    # TODO need to beef up the docs here

    Returns
    -------
    gain_img : ndarray

    """
    #namp = settings.spect[dnum]['numamplifiers'])
    #gains = settings.spect[dnum]['gain'][amp - 1]
    msgs.warn("Should probably be measuring the gain across the amplifier boundary")

    # Loop on amplifiers
    # ToDo
    # EMA --> I think there was a bug here.
    # the previous command was: gain_img = np.zeros_like(datasec_img)
    # but it returns an array of integers, so if the gain was <0.6 it
    # was rounded to 0 causing a lot of problems.
    gain_img = np.zeros_like(datasec_img,dtype=float)
    for ii in range(namp):
        amp = ii+1
        amppix = datasec_img == amp
        gain_img[amppix] = gain_list[ii]
    # Return
    return gain_img


def rn_frame(datasec_img, gain, ronoise, numamplifiers=1):
    """ Generate a RN image

    Parameters
    ----------

    Returns
    -------
    rn_img : ndarray
      Read noise *variance* image (i.e. RN**2)
    """
    _gain = np.asarray(gain) if isinstance(gain, (list, np.ndarray)) else np.array([gain])
    _ronoise = np.asarray(ronoise) if isinstance(ronoise, (list, np.ndarray)) \
                        else np.array([ronoise])
    if len(_gain) != numamplifiers:
        raise ValueError('Must provide a gain for each amplifier.')
    if len(_ronoise) != numamplifiers:
        raise ValueError('Must provide a read-noise for each amplifier.')
    if np.any(datasec_img > numamplifiers):
        raise ValueError('Pixel amplifier IDs do not match number of amplifiers.')

    # ToDO We should not be using numpy masked arrays!!!

    # Get the amplifier indices
    indx = datasec_img.astype(int) == 0
    amp = np.ma.MaskedArray(datasec_img.astype(int) - 1, mask=indx).filled(0)

    # Return the read-noise image.  Any pixels without an assigned
    # amplifier are given a noise of 0.
    return np.ma.MaskedArray(np.square(_ronoise[amp]) + np.square(0.5*_gain[amp]),
                             mask=indx).filled(0.0)


def subtract_overscan(rawframe, numamplifiers, datasec, oscansec, method='savgol', params=[5, 65]):
    """
    Subtract overscan

    Args:
        frame (:obj:`numpy.ndarray`):
            Frame from which to subtract overscan
        numamplifiers (int):
            Number of amplifiers for this detector.
        datasec (list):
            List of slices, one per amplifier, that contain the data in
            the raw frame.  The slices and be lists of slice ojects or
            strings.  If they are strings, :func:`parse.sec2slice` is
            used to convert them for use in the function.
        oscansec (list):
            List of slices, one per amplifier, that contain the
            overscane regions in the raw frame.  The slices and be lists
            of slice ojects or strings.  If they are strings,
            :func:`parse.sec2slice` is used to convert them for use in
            the function.
        method (:obj:`str`, optional):
            The method used to fit the overscan region.  Options are
            polynomial, savgol, median.
        params (:obj:`list`, optional):
            Parameters for the overscan subtraction.  For
            method=polynomial, set params = order, number of pixels,
            number of repeats ; for method=savgol, set params = order,
            window size ; for method=median, params are ignored.

    Returns:
        :obj:`numpy.ndarray`: The input frame with the overscan region
        subtracted
    """
    # Check input
    if len(datasec) != numamplifiers or len(oscansec) != numamplifiers:
        raise ValueError('Number of amplifiers does not match provided image sections.')

    # If the input image sections are strings, convert them
    if isinstance(datasec[0], str):
        _datasec = datasec.copy()
        for i in range(numamplifiers):
            _datasec[i] = parse.sec2slice(datasec[i], require_dim=2)
    else:
        _datasec = datasec
            
    if isinstance(oscansec[0], str):
        _oscansec = oscansec.copy()
        for i in range(numamplifiers):
            _oscansec[i] = parse.sec2slice(oscansec[i], require_dim=2)
    else:
        _oscansec = oscansec
    
    # Check that there are no overlapping data sections
    testframe = np.zeros_like(rawframe, dtype=int)
    for i in range(numamplifiers):
        testframe[_datasec[i]] += 1
    if np.any(testframe > 1):
        raise ValueError('Image has overlapping data sections!')

    # Copy the data so that the subtraction is not done in place
    nobias = rawframe.copy()

    # Perform the bias subtraction for each amplifier
    for i in range(numamplifiers):
        # Pull out the overscan data
        overscan = rawframe[_oscansec[i]]

        # Shape along at least one axis must match
        data_shape = rawframe[_datasec[i]].shape
        if not np.any([ dd == do for dd, do in zip(data_shape, overscan.shape)]):
            msgs.error('Overscan sections do not match amplifier sections for'
                       'amplifier {0}'.format(i+1))
        compress_axis = 1 if data_shape[0] == overscan.shape[0] else 0
        
        # Fit/Model the overscan region
        osfit = np.median(overscan) if method.lower() == 'median' \
                        else np.median(overscan, axis=compress_axis) 
        if method.lower() == 'polynomial':
            # TODO: Use np.polynomial.polynomial.polyfit instead?
            c = np.polyfit(np.arange(osfit.size), osfit, params[0])
            ossub = np.polyval(c, np.arange(osfit.size))
        elif method.lower() == 'savgol':
            ossub = signal.savgol_filter(osfit, params[1], params[0])
        elif method.lower() == 'median':
            # Subtract scalar and continue
            nobias[_datasec[i]] -= osfit
            continue
        else:
            raise ValueError('Unrecognized overscan subtraction method: {0}'.format(method))

        # Subtract along the appropriate axis
        nobias[_datasec[i]] -= (ossub[:,None] if compress_axis == 1 else ossub[None,:])

    return nobias



#def sub_overscan(rawframe, numamplifiers, datasec, oscansec, method='savgol', params=[5, 65]):
#    """
#    Subtract overscan
#
#    Args:
#        frame (:obj:`numpy.ndarray`):
#            Frame from which to subtract overscan
#        numamplifiers (int):
#            Number of amplifiers for this detector.
#        datasec (list):
#            Specifies the data sections, one sub-list per amplifier
#        oscansec (list):
#            Specifies the overscan sections, one sub-list per amplifier
#        method (:obj:`str`, optional):
#            The method used to fit the overscan region.  Options are
#            polynomial, savgol, median.
#        params (:obj:`list`, optional):
#            Parameters for the overscan subtraction.  For
#            method=polynomial, set params = order, number of pixels,
#            number of repeats ; for method=savgol, set params = order,
#            window size ; for method=median, params are ignored.
#    Returns:
#        :obj:`numpy.ndarray`: The input frame with the overscan region
#        subtracted
#    """
#    for i in range(numamplifiers):
#        # Determine the section of the chip that contains data
#        dx0, dx1 = datasec[i][0][0], datasec[i][0][1]
#        dy0, dy1 = datasec[i][1][0], datasec[i][1][1]
#        if dx0 < 0: dx0 += rawframe.shape[0]
#        if dx1 <= 0: dx1 += rawframe.shape[0]
#        if dy0 < 0: dy0 += rawframe.shape[1]
#        if dy1 <= 0: dy1 += rawframe.shape[1]
#        xds = np.arange(dx0, dx1)
#        yds = np.arange(dy0, dy1)
#
#        # Determine the section of the chip that contains the overscan
#        # region
#        ox0, ox1 = oscansec[i][0][0], oscansec[i][0][1]
#        oy0, oy1 = oscansec[i][1][0], oscansec[i][1][1]
#        if ox0 < 0: ox0 += rawframe.shape[0]
#        if ox1 <= 0: ox1 += min(rawframe.shape[0], dx1)  # Truncate to datasec
#        if oy0 < 0: oy0 += rawframe.shape[1]
#        if oy1 <= 0: oy1 += min(rawframe.shape[1], dy1)  # Truncate to datasec
#        xos = np.arange(ox0, ox1)
#        yos = np.arange(oy0, oy1)
#        w = np.ix_(xos, yos)
#        oscan = rawframe[w]
#
#        # Make sure the overscan section has at least one side consistent with datasec
#        if dx1-dx0 == ox1-ox0:
#            osfit = np.median(oscan, axis=1)  # Mean was hit by CRs
#        elif dy1-dy0 == oy1-oy0:
#            osfit = np.median(oscan, axis=0)
#        elif method.lower() == 'median':
#            osfit = np.median(oscan)
#        else:
#            msgs.error('Overscan sections do not match amplifier sections for'
#                       'amplifier {0}'.format(i+1))
#
#        # Fit/Model the overscan region
#        if method.lower() == 'polynomial':
#            c = np.polyfit(np.arange(osfit.size), osfit, params[0])
#            ossub = np.polyval(c, np.arange(osfit.size))#.reshape(osfit.size,1)
#        elif method.lower() == 'savgol':
#            ossub = signal.savgol_filter(osfit, params[1], params[0])
#        elif method.lower() == 'median':  # One simple value
#            ossub = osfit * np.ones(1)
#        else:
#            # TODO: Should we raise an exception instead?
#            msgs.warn('Unknown overscan subtraction method: {0}'.format(method))
#            msgs.info('Using a linear fit to the overscan region')
#            c = np.polyfit(np.arange(osfit.size), osfit, 1)
#            ossub = np.polyval(c, np.arange(osfit.size))#.reshape(osfit.size,1)
#
#        # Determine the section of the chip that contains data for this amplifier
#        if i==0:
#            frame = rawframe.copy()
#        wd = np.ix_(xds, yds)
#        ossub = ossub.reshape(osfit.size, 1)
#        if wd[0].shape[0] == ossub.shape[0]:
#            frame[wd] -= ossub
#        elif wd[1].shape[1] == ossub.shape[0]:
#            frame[wd] -= ossub.T
#        elif method.lower() == 'median':
#            frame[wd] -= osfit
#        else:
#            msgs.error("Could not subtract bias from overscan region --" 
#                       + msgs.newline() + "size of extracted regions does not match")
#
#    # Return
#    del xds, yds, xos, yos, oscan
#    return frame


def replace_columns(img, bad_cols, replace_with='mean'):
    """ Replace bad columns with values from the neighbors

    Parameters
    ----------
    img : ndarray
    bad_cols: ndarray (bool, 1D, shape[1] of img)
      True = bad column
      False = ok column
    replace_with : str, optional
      Option for replacement
       mean -- Use the mean of the closest left/right columns

    Returns
    -------
    img2 : ndarray
      Copy of the input image with the bad columns replaced
    """
    # Prep
    img2 = img.copy()
    # Find the starting/ends of the bad column sets
    tmp = np.zeros(img.shape[1], dtype=int)
    tmp[bad_cols] = 1
    tmp2 = tmp - np.roll(tmp,1)
    # Deal with first column
    if bad_cols[0]:
        tmp2[0]=1
    # Deal with last column
    if bad_cols[-1]:
        tmp2[-1]=-1
    ledges = np.where(tmp2 == 1)[0]
    redges = np.where(tmp2 == -1)[0]
    # Last column?
    if tmp2[-1] == 1:
        redges = np.concatenate([redges, np.array([bad_cols.size-1])])
    # Loop on em
    for kk, ledge in enumerate(ledges):
        lval = img[:,ledge-1]
        rval = img[:,redges[kk]]
        # Replace
        if replace_with == 'mean':
            mval = (lval+rval)/2.
            for ii in range(ledge, redges[kk]+1):
                img2[:,ii] = mval
        else:
            msgs.error("Bad option to replace_columns")
    # Return
    return img2


def trim_frame(frame, mask):
    """
    Trim the masked regions from a frame.

    Args:
        frame (:obj:`numpy.ndarray`):
            Image to be trimmed
        mask (:obj:`numpy.ndarray`):
            Boolean image set to True for values that should be trimmed
            and False for values to be returned in the output trimmed
            image.

    Return:
        :obj:`numpy.ndarray`:
            Trimmed image

    Raises:
        PypitError:
            Error raised if the trimmed image includes masked values
            because the shape of the valid region is odd.
    """
    # TODO: Should check for this failure mode earlier
    if np.any(mask[np.invert(np.all(mask,axis=1)),:][:,np.invert(np.all(mask,axis=0))]):
        msgs.error('Data section is oddly shaped.  Trimming does not exclude all '
                   'pixels outside the data sections.')
    return frame[np.invert(np.all(mask,axis=1)),:][:,np.invert(np.all(mask,axis=0))]

#def trim(frame, numamplifiers, datasec):
#    """ Core method to trim an input image
#
#    Parameters
#    ----------
#    frame : ndarray
#    numamplifiers : int
#    datasec : list of datasecs
#      One per amplifier
#
#    Returns
#    -------
#    frame : ndarray
#      Trimmed
#    """
#    for i in range(numamplifiers):
#        #datasec = "datasec{0:02d}".format(i+1)
#        #x0, x1 = settings.spect[dnum][datasec][0][0], settings.spect[dnum][datasec][0][1]
#        #y0, y1 = settings.spect[dnum][datasec][1][0], settings.spect[dnum][datasec][1][1]
#        x0, x1 = datasec[i][0][0], datasec[i][0][1]
#        y0, y1 = datasec[i][1][0], datasec[i][1][1]
#        # Fuss with edges
#        if x0 < 0:
#            x0 += frame.shape[0]
#        if x1 <= 0:
#            x1 += frame.shape[0]
#        if y0 < 0:
#            y0 += frame.shape[1]
#        if y1 <= 0:
#            y1 += frame.shape[1]
#        if i == 0:
#            xv = np.arange(x0, x1)
#            yv = np.arange(y0, y1)
#        else:
#            xv = np.unique(np.append(xv, np.arange(x0, x1)))
#            yv = np.unique(np.append(yv, np.arange(y0, y1)))
#    # Construct and array with the rows and columns to be extracted
#    w = np.ix_(xv, yv)
##	if len(file.shape) == 2:
##		trimfile = file[w]
##	elif len(file.shape) == 3:
##		trimfile = np.zeros((w[0].shape[0],w[1].shape[1],file.shape[2]))
##		for f in range(file.shape[2]):
##			trimfile[:,:,f] = file[:,:,f][w]
##	else:
##		msgs.error("Cannot trim {0:d}D frame".format(int(len(file.shape))))
#    try:
#        return frame[w]
#    except:
#        msgs.bug("Odds are datasec is set wrong. Maybe due to transpose")
#        debugger.set_trace()
#        msgs.error("Cannot trim file")

def variance_frame(datasec_img, sciframe, gain, ronoise, numamplifiers=1, darkcurr=None,
                   exptime=None, skyframe=None, objframe=None, adderr=0.01):
    """
    Calculate the variance image including detector noise.

    .. todo::
        This needs particular attention because exptime and darkcurr;
        used to be dnoise

    Args:
        datasec_img (:obj:`numpy.ndarray`):
            Image that identifies which amplifier (1-indexed) was used
            to read each pixel.  Anything less than 1 is ignored.
        sciframe (:obj:`numpy.ndarray`):
            Science frame with counts in ?
        gain (:obj:`float`, array-like):
            Gain for each amplifier
        ronoise (:obj:`float`, array-like):
            Read-noise for each amplifier
        numamplifiers (:obj:`int`, optional):
            Number of amplifiers.  Default is 1.  (TODO: This is
            superfluous.  Could get the number of amplifiers from the
            maximum value in datasec_img or the length of the
            gain/ronoise lists.)
        ronoise (:obj:`float`, array-like):

        darkcurrent (:noise (:

        adderr: float, default = 0.01
            Error floor. The quantity adderr**2*sciframe**2 is added in qudarature to the variance to ensure that the
            S/N is never > 1/adderr, effectively setting a floor on the noise or a ceiling on the S/N.

    objframe : ndarray, optional
      Model of object counts
    Returns
    -------
    variance image : ndarray
    """

    # ToDO JFH: I would just add the darkcurrent here into the effective read noise image
    # The effective read noise (variance image)
    rnoise = rn_frame(datasec_img, gain, ronoise, numamplifiers=numamplifiers)

    # No sky frame provided
    if skyframe is None:
        _darkcurr = 0 if darkcurr is None else darkcurr
        if exptime is not None:
            _darkcurr *= exptime/3600.
        var = np.abs(sciframe - np.sqrt(2.0)*np.sqrt(rnoise)) + rnoise + _darkcurr
        var = var + adderr**2*(np.abs(sciframe))**2
        return var

    # TODO: There's some complicated logic here.  Why is objframe
    # needed?  Can't a users just use objframe in place of sciframe and
    # get the same behavior?  Why is darkcurr (what was dnoise) used
    # with sciframe and not objframe?

    # ToDO JFH: shouldn't dark current be added here as well??
    _objframe = np.zeros_like(skyframe) if objframe is None else objframe
    var = np.abs(skyframe + _objframe - np.sqrt(2.0)*np.sqrt(rnoise)) + rnoise
    var = var + adderr ** 2 * (np.abs(sciframe)) ** 2
    return





