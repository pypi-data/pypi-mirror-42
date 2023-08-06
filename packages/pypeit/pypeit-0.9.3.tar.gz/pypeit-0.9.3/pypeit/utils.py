

import itertools
import matplotlib

import numpy as np

from scipy.optimize import curve_fit
from scipy import interpolate

from astropy import units
from matplotlib import pyplot as plt

# Imports for fast_running_median
from collections import deque
from itertools import islice
from bisect import insort, bisect_left
from pypeit.core import pydl
from pypeit import msgs

def wavegrid(wave_min, wave_max, dwave, osamp=1.0):
    """
    Utility routine to generate a uniform grid of wavelengths
    Args:
        wave_min: float
           Mininum wavelength. Can be in linear or log.
        wave_max: float
           Maximum wavelength. Can be in linear or log.
        dwave: float
           Delta wavelength interval
        osamp: float
           Oversampling factor

    Returns:
        wave_grid: float ndarray
           Wavelength grid
    """

    ngrid = int(np.ceil((wave_max - wave_min)/dwave))
    wave_grid = wave_min + (dwave/osamp)*np.arange(int(np.ceil(osamp*ngrid)))
    return wave_grid


def rebin(a, newshape):
    '''Rebin an array to a new shape using slicing. This routine is taken from:
    https://scipy-cookbook.readthedocs.io/items/Rebinning.html. The image shapes need
    not be integer multiples of each other, but in this regime the transformation will
    not be reversible, i.e. if a_orig = rebin(rebin(a,newshape), a.shape) then
    a_orig will not be everywhere equal to a (but it will be equal in most places).

    Args:
        a: ndarray, any dtype
          Image of any dimensionality and data type
        newshape:
          Shape of the new image desired. Dimensionality must be the same as a.
    Returns:
        ndarray: same dtype as input Image with same values as a rebinning to shape newshape
    '''

    if not len(a.shape) == len(newshape):
        msgs.error('Dimension of a image does not match dimension of new requested image shape')

    slices = [slice(0, old, float(old) / new) for old, new in zip(a.shape, newshape)]
    coordinates = np.mgrid[slices]
    indices = coordinates.astype('i')  # choose the biggest smaller integer index
    return a[tuple(indices)]

# TODO This function is only used by procimg.lacosmic. Can it be replaced by above?
def rebin_evlist(frame, newshape):
    # This appears to be from
    # https://scipy-cookbook.readthedocs.io/items/Rebinning.html
    shape = frame.shape
    lenShape = len(shape)
    factor = np.asarray(shape)/np.asarray(newshape)
    evList = ['frame.reshape('] + \
             ['int(newshape[%d]),int(factor[%d]),'% (i, i) for i in range(lenShape)] + \
             [')'] + ['.sum(%d)' % (i+1) for i in range(lenShape)] + \
             ['/factor[%d]' % i for i in range(lenShape)]
    return eval(''.join(evList))




def pyplot_rcparams():
    """
    params for pretty matplotlib plots

    Returns:

    """
    # set some plotting parameters
    plt.rcParams["xtick.top"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["xtick.minor.visible"] = True
    plt.rcParams["ytick.minor.visible"] = True
    plt.rcParams["ytick.direction"] = 'in'
    plt.rcParams["xtick.direction"] = 'in'
    plt.rcParams["xtick.major.size"] = 6
    plt.rcParams["ytick.major.size"] = 6
    plt.rcParams["xtick.minor.size"] = 3
    plt.rcParams["ytick.minor.size"] = 3
    plt.rcParams["xtick.major.width"] = 1
    plt.rcParams["ytick.major.width"] = 1
    plt.rcParams["xtick.minor.width"] = 1
    plt.rcParams["ytick.minor.width"] = 1
    plt.rcParams["axes.linewidth"] = 1
    plt.rcParams["lines.linewidth"] = 3
    plt.rcParams["lines.markeredgewidth"] = 2
    plt.rcParams["patch.linewidth"] = 3
    plt.rcParams["hatch.linewidth"] = 3
    plt.rcParams["font.size"] = 13
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.handletextpad"] = 1


def pyplot_rcparams_default():
    """
    restore default rcparams

    Returns:

    """
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)


def smooth(x, window_len, window='flat'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that edge effects are minimize at the beginning and end part of the signal.

     This code taken from this cookbook and slightly modified: https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing., default is 'flat'

    output:
        the smoothed signal, same shape as x

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='same')

    return y[(window_len-1):(y.size-(window_len-1))]


def fast_running_median(seq, window_size):
    """
    Compute the median of sequence of numbers with a running window. The boundary conditions are identical to the
    scipy 'reflect' boundary codition:

     'reflect' (`d c b a | a b c d | d c b a`)
     The input is extended by reflecting about the edge of the last pixel.

    This code has been confirmed to produce identical results to scipy.ndimage.filters.median_filter with the reflect
    boundary condition, but is ~ 100 times faster.

    Args:
        seq (list or 1-d numpy array of numbers):
        window_size (int): size of running window.

    Returns:
        ndarray: median filtered values

    Code contributed by Peter Otten, made to be consistent with scipy.ndimage.filters.median_filter by Joe Hennawi.

    See discussion at:
    http://groups.google.com/group/comp.lang.python/browse_thread/thread/d0e011c87174c2d0
    """
    # pad the array for the reflection
    seq_pad = np.concatenate((seq[0:window_size][::-1],seq,seq[-1:(-1-window_size):-1]))

    window_size= int(window_size)
    seq_pad = iter(seq_pad)
    d = deque()
    s = []
    result = []
    for item in islice(seq_pad, window_size):
        d.append(item)
        insort(s, item)
        result.append(s[len(d)//2])
    m = window_size // 2
    for item in seq_pad:
        old = d.popleft()
        d.append(item)
        del s[bisect_left(s, old)]
        insort(s, item)
        result.append(s[m])

    # This takes care of the offset produced by the original code deducec by trial and error comparison with
    # scipy.ndimage.filters.medfilt

    result = np.roll(result, -window_size//2 + 1)
    return result[window_size:-window_size]


# TODO JFH: This is the old bspline_fit which shoul be deprecated. I think some codes still use it though. We should transtion to pydl everywhere
def bspline_fit(x,y,order=3,knots=None,everyn=20,xmin=None,xmax=None,w=None,bkspace=None):
    """ bspline fit to x,y
    Should probably only be called from func_fit

    Parameters:
    ---------
    x: ndarray
    y: ndarray
    func: str
      Name of the fitting function:  polynomial, legendre, chebyshev, bspline
    deg: int 
      deg of the spline.  Default=3 (cubic)
    xmin: float, optional
      Minimum value in the array  [both must be set to normalize]
    xmax: float, optional
      Maximum value in the array  [both must be set to normalize]
    w: ndarray, optional
      weights to be used in the fitting (weights = 1/sigma)
    knots: ndarray, optional
      Internal knots only.  External ones are added by scipy
    everyn: int 
      Knot everyn good pixels, if used
    bkspace: float 
      Spacing of breakpoints in units of x

    Returns:
    ---------
    tck : tuple
      describes the bspline
    """
    task = 0  # Default of splrep
    if w is None:
        ngd = x.size
        gd = np.arange(ngd)
        weights = None
    else:
        gd = np.where(w > 0.)[0]
        weights = w[gd]
        ngd = len(gd)
    # Make the knots
    if knots is None:
        if bkspace is not None: 
            xrnge = (np.max(x[gd]) - np.min(x[gd]))
            startx = np.min(x[gd])
            nbkpts = max(int(xrnge/bkspace) + 1,2)
            tempbkspace = xrnge/(nbkpts-1)
            knots = np.arange(1, nbkpts-1)*tempbkspace + startx
            # Remove cases where two knots have no data between them
            keep_knots = np.array([True]*len(knots))
            for ii in range(1,len(knots)): # Ugly for loop..
                if not np.any((x[gd] > knots[ii-1]) & (x[gd] < knots[ii])):
                    keep_knots[ii] = False
            knots = knots[keep_knots]
        elif everyn is not None:
            # A knot every good N pixels
            idx_knots = np.arange(everyn//2, ngd-everyn//2, everyn)
            knots = x[gd[idx_knots]]
        else:
            msgs.error("No method specified to generate knots")
    else:
        task = -1
    # Generate spline
    try:
        tck = interpolate.splrep(x[gd], y[gd], w=weights, k=order, xb=xmin, xe=xmax, t=knots, task=task)
    except ValueError:
        # Knot problem (usually)
        msgs.warn("Problem in the bspline knot")
        raise ValueError("Crashing out of bspline fitting")
    return tck

#ToDo I would prefer to remove the kwargs_bspline and
# and make them explicit
def bspline_profile(xdata, ydata, invvar, profile_basis, inmask = None, upper=5, lower=5,
                    maxiter=25, nord = 4, bkpt=None, fullbkpt=None,
                    relative=None, kwargs_bspline={}, kwargs_reject={}):
    """
    Create a B-spline in the least squares sense with rejection, using a model profile

     Parameters
     ----------
     xdata : :class:`numpy.ndarray`
         Independent variable.
     ydata : :class:`numpy.ndarray`
         Dependent variable.
     invvar : :class:`numpy.ndarray`
         Inverse variance of `ydata`.
     profile_basis : :class:`numpy.ndarray`
         model profiles
     upper : :class:`int` or :class:`float`, optional
         Upper rejection threshold in units of sigma, defaults to 5 sigma.
     lower : :class:`int` or :class:`float`, optional
         Lower rejection threshold in units of sigma, defaults to 5 sigma.
     maxiter : :class:`int`, optional
         Maximum number of rejection iterations, default 10.  Set this to
         zero to disable rejection.
     nord : :class:`int`, optional
         Order of B-spline fit
     bkpt : :class:`numpy.ndarray`
         Array of breakpoints to be used for the b-spline
     fullbkpt : :class:`numpy.ndarray`
         Full array of breakpoints to be used for the b-spline, without letting the b-spline class append on any extra bkpts
     relative : class:`numpy.ndarray`
        Array of integer indices to be used for computing the reduced chi^2 of the fits, which then is used as a scale factor for
         the upper,lower rejection thresholds
     kwargs_bspline : dict
       Passed to bspline
     kwargs_reject : dict
       Passed to djs_reject

     Returns
     -------
     :func:`tuple`
         A tuple containing the (sset, outmask, yfit, reduced_chi), where

            sset: object
               bspline object
            outmask: : :class:`numpy.ndarray`
               output mask which the same size as xdata, such that rejected points have outmask set to False
            yfit  : :class:`numpy.ndarray`
               result of the bspline fit (same size as xdata)
            reduced_chi: float
               value of the reduced chi^2
     """
    # Checks
    nx = xdata.size
    if ydata.size != nx:
        msgs.error('Dimensions of xdata and ydata do not agree.')

    # ToDO at the moment invvar is a required variable input
    #    if invvar is not None:
    #        if invvar.size != nx:
    #            raise ValueError('Dimensions of xdata and invvar do not agree.')
    #        else:
    #            #
    #            # This correction to the variance makes it the same
    #            # as IDL's variance()
    #            #
    #            var = ydata.var()*(float(nx)/float(nx-1))
    #            if var == 0:
    #                var = 1.0
    #            invvar = np.ones(ydata.shape, dtype=ydata.dtype)/var

    npoly = int(profile_basis.size/nx)
    if profile_basis.size != nx*npoly:
        msgs.error('Profile basis is not a multiple of the number of data points.')

    # Init
    yfit = np.zeros(ydata.shape)
    reduced_chi = 0.

    if invvar.size == 1:
        outmask = True
    else:
        outmask = np.ones(invvar.shape, dtype='bool')

    if inmask is None:
        inmask = (invvar > 0)

    nin = np.sum(inmask)
    msgs.info("Fitting npoly =" + "{:3d}".format(npoly) + " profile basis functions, nin=" + "{:3d}".format(nin) + " good pixels")
    msgs.info("******************************  Iter  Chi^2  # rejected  Rel. fact   ******************************")
    msgs.info("                              ----  -----  ----------  --------- ")


    maskwork = outmask & inmask & (invvar > 0)
    if not maskwork.any():
        msgs.error('No valid data points in bspline_profile!.')
    else:
        # Init bspline class
        sset = pydl.bspline(xdata[maskwork], nord=nord, npoly=npoly, bkpt=bkpt, fullbkpt=fullbkpt,
                                funcname='Bspline longslit special', **kwargs_bspline)
        if maskwork.sum() < sset.nord:
            msgs.warn('Number of good data points fewer than nord.')
            exit_status = 4
            return sset, outmask, yfit, reduced_chi, exit_status

    # This was checked in detail against IDL for identical inputs
    outer = (np.outer(np.ones(nord, dtype=float), profile_basis.flatten('F'))).T
    action_multiple = outer.reshape((nx, npoly * nord), order='F')
    #--------------------
    # Iterate spline fit
    iiter = 0
    error = -1
    qdone = False
    exit_status = 0
    relative_factor = 1.0
    tempin = np.copy(inmask)
    while (error != 0 or qdone is False) and iiter <= maxiter and (exit_status == 0):
        ngood = maskwork.sum()
        goodbk = sset.mask.nonzero()[0]
        if ngood <= 1 or not sset.mask.any():
            sset.coeff = 0
            exit_status = 2 # This will end iterations
            #iiter = maxiter + 1 # End iterations
        else:
            # Do the fit. Return values from workit for error are as follows:
            #    0 if fit is good
            #   -1 if some breakpoints are masked, so try the fit again
            #   -2 if everything is screwed

            # we'll do the fit right here..............
            if error != 0:
                bf1, laction, uaction = sset.action(xdata)
                if np.any(bf1 == -2) or (bf1.size !=nx*nord):
                    msgs.error("BSPLINE_ACTION failed!")
                action = np.copy(action_multiple)
                for ipoly in range(npoly):
                    action[:, np.arange(nord)*npoly + ipoly] *= bf1
                del bf1 # Clear the memory
            if np.sum(np.isfinite(action) is False) > 0:
                msgs.error("Infinities in action matrix, wavelengths may be very messed up!!!")
            error, yfit = sset.workit(xdata, ydata, invvar*maskwork,action, laction, uaction)
        iiter += 1
        if error == -2:
            msgs.warn(" All break points have been dropped!! Fit failed, I hope you know what you are doing")
            exit_status = 3
            return (sset, np.zeros(xdata.shape,dtype=bool), np.zeros(xdata.shape), reduced_chi, exit_status)
        elif error == 0:
            # Iterate the fit -- next rejection iteration
            chi_array = (ydata - yfit)*np.sqrt(invvar * maskwork)
            reduced_chi = np.sum(chi_array**2)/(ngood - npoly*(len(goodbk) + nord)-1)
            relative_factor = 1.0
            # JFH -- What is
            if relative is not None:
                nrel = len(relative)
                if nrel == 1:
                    relative_factor = np.sqrt(reduced_chi)
                else:
                    this_chi2 = np.sum(chi_array[relative]**2)/(nrel - (len(goodbk) + nord) - 1)
                    relative_factor = np.sqrt(this_chi2)
                relative_factor = max(relative_factor,1.0)
            # Rejection
            # ToDO JFH by setting inmask to be tempin which is maskwork, we are basically implicitly enforcing sticky rejection
            # here. See djs_reject.py. I'm leaving this as is for consistency with the IDL version, but this may require
            # further consideration. I think requiring sticky to be set is the more transparent behavior.
            maskwork, qdone = pydl.djs_reject(ydata, yfit, invvar=invvar,
                                         inmask=tempin, outmask=maskwork,
                                         upper=upper*relative_factor,
                                         lower=lower*relative_factor, **kwargs_reject)
            tempin = np.copy(maskwork)
            msgs.info("                             {:4d}".format(iiter) + "{:8.3f}".format(reduced_chi) +
                      "  {:7d}".format((maskwork == 0).sum()) + "      {:6.2f}".format(relative_factor))

        else:
            msgs.info("                             {:4d}".format(iiter) + "    ---    ---    ---    ---")

    if iiter == (maxiter + 1):
        exit_status = 1

    # Exit status:
    #    0 = fit exited cleanly
    #    1 = maximum iterations were reached
    #    2 = all points were masked
    #    3 = all break points were dropped
    #    4 = Number of good data points fewer than nord

    msgs.info("***************************************************************************************************")
    msgs.info(
        "Final fit after " + "{:2d}".format(iiter) + " iterations: reduced_chi = " + "{:8.3f}".format(reduced_chi) +
        ", rejected = " + "{:7d}".format((maskwork == 0).sum()) + ", relative_factor = {:6.2f}".format(relative_factor))
    # Finish
    outmask = np.copy(maskwork)
    # Return
    return sset, outmask, yfit, reduced_chi, exit_status



def calc_ivar(varframe):
    """ Calculate the inverse variance based on the input array

    Args:
        varframe (ndarray):  Variance image

    Returns:
        ndarray:  Inverse variance image
    """
    ivar = (varframe > 0.) / (np.abs(varframe) + (varframe == 0))
    return ivar



def func_fit(x, y, func, deg, x2 = None, minx=None, maxx=None, minx2=None, maxx2=None, w=None, inmask = None, guesses=None,
             bspline_par=None, return_errors=False):
    """ General routine to fit a function to a given set of x,y points

    Parameters
    ----------
    x : ndarray
    y : ndarray
    func : str
      polynomial, legendre, chebyshev, bspline, gaussian
    deg : int
      degree of the fit
    minx : float, optional
    maxx
    w
    guesses : tuple
    bspline_par : dict
      Passed to bspline_fit()

    Returns
    -------
    coeff : ndarray or tuple
      ndarray for standard function fits
      tuple for bspline

    """

    # If the user provided an inmask apply it. The logic below of evaluating the fit only at the non-masked
    # pixels is preferable to the other approach of simply setting the weights to zero. The reason for that is that
    # the fits use a least-square optimization approach using matrix algebra, and lots of zero weights are
    # 1) more costly, and 2) will not produce exactly the same result (due to roundoff error) as actually
    # removing the locations you want to mask.
    if inmask is not None:
        x_out = x[inmask]
        y_out = y[inmask]
        if x2 is not None:
            x2_out = x2[inmask]
        else:
            x2_out = None
        if w is not None:
            w_out = w[inmask]
        else:
            w_out = None
    else:
        x_out = x
        y_out = y
        if x2 is not None:
            x2_out = x2
        else:
            x2_out = None
        if w is not None:
            w_out = w
        else:
            w_out = None

    # For two-d fits x = x, y = x2, y = z
    if ('2d' in func) and (x2_out is not None):
        # Is this a 2d fit?
        return polyfit2d_general(x_out, x2_out, y_out, deg, w=w_out, function=func[:-2],minx=minx, maxx=maxx, miny=minx2, maxy=maxx2)
    elif func == "polynomial":
        return np.polynomial.polynomial.polyfit(x_out, y_out, deg, w=w_out)
    elif func == "legendre":
        if minx is None or maxx is None:
            if np.size(x_out) == 1:
                xmin, xmax = -1.0, 1.0
            else:
                xmin, xmax = np.min(x_out), np.max(x_out)
        else:
            xmin, xmax = minx, maxx
        xv = 2.0 * (x_out-xmin)/(xmax-xmin) - 1.0
        return np.polynomial.legendre.legfit(xv, y_out, deg, w=w_out)
    elif func == "chebyshev":
        if minx is None or maxx is None:
            if np.size(x_out) == 1:
                xmin, xmax = -1.0, 1.0
            else:
                xmin, xmax = np.min(x_out), np.max(x_out)
        else:
            xmin, xmax = minx, maxx
        xv = 2.0 * (x_out-xmin)/(xmax-xmin) - 1.0
        return np.polynomial.chebyshev.chebfit(xv, y_out, deg, w=w_out)
    elif func == "bspline":
        if bspline_par is None:
            bspline_par = {}
        # TODO -- Deal with this kwargs-like kludge
        return bspline_fit(x_out, y_out, order=deg, w=w_out, **bspline_par)
    elif func == "gaussian":
        # Guesses
        if guesses is None:
            ampl, cent, sigma = guess_gauss(x_out, y_out)
            # As first guess choose slope and intercept to be zero
            b = 0
            m = 0
        else:
            if deg == 2:
                ampl, sigma = guesses
            elif deg == 3:
                ampl, cent, sigma = guesses
            elif deg == 4:
                b, ampl, cent, sigma = guesses
            elif deg == 5:
                m, b, ampl, cent, sigma = guesses
        # Error
        if w_out is not None:
            sig_y = 1./w_out
        else:
            sig_y = None
        if deg == 2:  # 2 parameter fit
            popt, pcov = curve_fit(gauss_2deg, x_out, y_out, p0=[ampl, sigma], sigma=sig_y)
        elif deg == 3:  # Standard 3 parameters
            popt, pcov = curve_fit(gauss_3deg, x_out, y_out, p0=[ampl, cent, sigma],
                                   sigma=sig_y)
        elif deg == 4:  # 4 parameters
            popt, pcov = curve_fit(gauss_4deg, x_out, y_out, p0=[b, ampl, cent, sigma],sigma=sig_y)
        elif deg == 5:  # 5 parameters
            popt, pcov = curve_fit(gauss_5deg, x_out, y_out, p0=[m, b, ampl, cent, sigma],sigma=sig_y)
        else:
            msgs.error("Not prepared for deg={:d} for Gaussian fit".format(deg))
        # Return
        if return_errors:
            return popt, pcov
        else:
            return popt
    elif func == "moffat":
        # Guesses
        if guesses is None:
            ampl, cent, sigma = guess_gauss(x_out, y_out)
            p0 = ampl
            p2 = 3. # Standard guess
            p1 = (2.355*sigma)/(2*np.sqrt(2**(1./p2)-1))
        else:
            p0,p1,p2 = guesses
        # Error
        if w_out is not None:
            sig_y = 1./w_out
        else:
            sig_y = None
        if deg == 3:  # Standard 3 parameters
            popt, pcov = curve_fit(moffat, x_out, y_out, p0=[p0,p1,p2], sigma=sig_y)
        else:
            msgs.error("Not prepared for deg={:d} for Moffat fit".format(deg))
        # Return
        return popt
    else:
        msgs.error("Fitting function '{0:s}' is not implemented yet" + msgs.newline() +
                   "Please choose from 'polynomial', 'legendre', 'chebyshev','bspline'")


def func_val(c, x, func, x2 = None, minx=None, maxx=None, minx2=None, maxx2=None):
    """ Generic routine to return an evaluated function
    Functional forms include:
      polynomial, legendre, chebyshev, bspline, gauss

    Parameters
    ----------
    c : ndarray
      coefficients
    x
    func
    minx
    maxx

    Returns
    -------
    values : ndarray

    """
    # For two-d fits x = x, y = x2, y = z
    if ('2d' in func) and (x2 is not None):
        # Is this a 2d fit?
        if func[:-2] == "polynomial":
            return np.polynomial.polynomial.polyval2d(x, x2, c)
        elif func[:-2] in ["legendre", "chebyshev"]:
            # Scale x-direction
            xv = scale_minmax(x, minx=minx, maxx=maxx)
            # Scale x2-direction
            x2v = scale_minmax(x2, minx=minx2, maxx=maxx2)
            if func[:-2] == "legendre":
                return np.polynomial.legendre.legval2d(xv, x2v, c)
            elif func[:-2] == "chebyshev":
                return np.polynomial.chebyshev.chebval2d(xv, x2v, c)
        else:
            msgs.error("Function {0:s} has not yet been implemented for 2d fits".format(func))
        return None
    elif func == "polynomial":
        return np.polynomial.polynomial.polyval(x, c)
    elif func == "legendre":
        if minx is None or maxx is None:
            if np.size(x) == 1:
                xmin, xmax = -1.0, 1.0
            else:
                xmin, xmax = np.min(x), np.max(x)
        else:
            xmin, xmax = minx, maxx
        xv = 2.0 * (x-xmin)/(xmax-xmin) - 1.0
        return np.polynomial.legendre.legval(xv, c)
    elif func == "chebyshev":
        if minx is None or maxx is None:
            if np.size(x) == 1:
                xmin, xmax = -1.0, 1.0
            else:
                xmin, xmax = np.min(x), np.max(x)
        else:
            xmin, xmax = minx, maxx
        xv = 2.0 * (x-xmin)/(xmax-xmin) - 1.0
        return np.polynomial.chebyshev.chebval(xv, c)
    elif func == "bspline":
        return interpolate.splev(x, c, ext=1)
    elif func == "gaussian":
        if len(c) == 2:
            return gauss_2deg(x, c[0], c[1])
        elif len(c) == 3:
            return gauss_3deg(x, c[0], c[1], c[2])
        else:
            msgs.error("Not ready for this type of gaussian")
    elif func == "moffat":
        if len(c) == 3:
            return moffat(x, c[0], c[1], c[2])
        else:
            msgs.error("Not ready for this type of Moffat")
    else:
        msgs.error("Fitting function '{0:s}' is not implemented yet" + msgs.newline() +
                   "Please choose from 'polynomial', 'legendre', 'chebyshev', 'bspline'")


def calc_fit_rms(xfit, yfit, fit, func, minx=None, maxx=None, weights=None):
    """ Simple RMS calculation

    Args:
        xfit : ndarray
        yfit : ndarray
        fit : coefficients
        func : str
        minx : float, optional
        maxx : float, optional

    Returns:
        float: RMS

    """
    if weights is None:
        weights = np.ones(xfit.size)
    # Normalise
    weights /= np.sum(weights)
    values = func_val(fit, xfit, func, minx=minx, maxx=maxx)
    # rms = np.std(yfit-values)
    rms = np.sqrt(np.sum(weights*(yfit-values)**2))
    # Return
    return rms


def robust_meanstd(array):
    """
    Determine a robust measure of the mean and dispersion of array

    Args:
        array (ndarray): an array of values

    Returns:
        float, float: median of the array and a robust estimate of the standand deviation (assuming a symmetric distribution)
    """
    med = np.median(array)
    mad = np.median(np.abs(array-med))
    return med, 1.4826*mad



def polyfitter2d(data, mask=None, order=2):
    """
    2D fitter

    Args:
        data:
        mask:
        order:

    Returns:

    """
    x, y = np.meshgrid(np.linspace(0.0, 1.0, data.shape[1]), np.linspace(0.0, 1.0, data.shape[0]))
    if isinstance(mask, (float, int)):
        # mask is the value that should be masked in data
        w = np.where(data != mask)
        xf = x[w].flatten()
        yf = y[w].flatten()
        m = polyfit2d(xf, yf, data[w].T.flatten(), order)
    elif mask is None or mask.size == 0:
        # There are no masks
        xf = x.flatten()
        yf = y.flatten()
        m = polyfit2d(xf, yf, data.T.flatten(), order)
    elif len(mask.shape) == 1:
        # mask is applied along one axis
        mskar = np.ones((data.shape[0], data.shape[1]))
        mskar[mask, :] = 0
        w = np.where(mskar == 1)
        xf = x[w].flatten()
        yf = y[w].flatten()
        m = polyfit2d(xf, yf, data[w].T.flatten(), order)
    elif mask.shape[0] == data.shape[0] and mask.shape[1] == data.shape[1]:
        # mask is an array that indicates the masked data
        w = np.where(mask == 0)
        xf = x[w].flatten()
        yf = y[w].flatten()
        m = polyfit2d(xf, yf, data[w].T.flatten(), order)
    # Return the best model
    return m, polyval2d(x, y, m).T


def polyfit2d(x, y, z, order=3):
    """
    Generate 2D polynomial

    Args:
        x:
        y:
        z:
        order:

    Returns:

    """
    ncols = (order + 1)**2
    G = np.zeros((x.size, ncols))
    ij = itertools.product(range(order+1), range(order+1))
    for k, (i,j) in enumerate(ij):
        G[:,k] = x**i * y**j
    m, null, null, null = np.linalg.lstsq(G, z)
    return m


def polyval2d(x, y, m):
    """
    Generate 2D polynomial

    Args:
        x:
        y:
        m:

    Returns:

    """
    order = int(np.sqrt(len(m))) - 1
    ij = itertools.product(range(order+1), range(order+1))
    z = np.zeros_like(x)
    for a, (i, j) in zip(m, ij):
        z += a * x**i * y**j
    return z


def moffat(x,p0,p1,p2):
    """
    Moffat profile
    This 3 parameter formulation assumes the trace is known

    Args:
        x (float or ndarray): x values
        p0 (float): Amplitude
        p1 (float):
          Width scaling
        p2 : float

    Returns:
        float or ndarray: Evaluated Moffat
    """
    return p0 / (1+(x/p1)**2)**p2


def gauss_2deg(x,ampl,sigm):
    """
    Simple 2 parameter Gaussian (amplitude, sigma)

    Args:
        x
        ampl
        sigm

    Returns:
        float or ndarray: Evaluated Gausssian
    """
    return ampl*np.exp(-1.*x**2/2./sigm**2)


def gauss_3deg(x,ampl,cent,sigm):
    """  Simple 3 parameter Gaussian

    Args:
        x (float or ndarray): x-valus
        ampl (float): Amplitude
        cent (float): Centroid
        sigm (float): sigma

    Returns:
        float or ndarray: Evaluated Gausssian
    """
    return ampl*np.exp(-1.*(cent-x)**2/2/sigm**2)


def gauss_4deg(x,b, ampl,cent,sigm):
    """  Simple 3 parameter Gaussian

    Args:
        x
        b (float): Floor
        ampl (float): Amplitude
        cent (float): Centroid
        sigm (float): sigma

    Returns:
        float or ndarray: Evaluated Gausssian
    """
    return b + ampl*np.exp(-1.*(cent-x)**2/2/sigm**2)


def gauss_5deg(x,m, b, ampl,cent,sigm):
    """  Simple 3 parameter Gaussian

    Args:
        x
        m (float): Slope of floor
        b (float): Floor
        ampl (float): Amplitude
        cent (float): Centroid
        sigm (float): sigma

    Returns:
        float or ndarray: Evaluated Gausssian
    """
    return b + m*x + ampl*np.exp(-1.*(cent-x)**2/2/sigm**2)


def guess_gauss(x,y):
    """
    Guesses Gaussian parameters with basic stats

    Args:
        x (ndarray): x-values
        y (ndarray): y-values

    Returns:
        float, float, float:  Amplitude, centroid, sigma

    """
    ypos = y - y.min()
    cent = np.sum(ypos*x)/np.sum(ypos)
    sigma = np.sqrt(np.abs(np.sum((x-cent)**2*ypos)/np.sum(ypos))) # From scipy doc
    # Calculate ampl from pixels within +/- sigma/2
    cen_pix= np.abs(x-cent)<sigma/2
    if np.any(cen_pix):
        ampl = np.median(y[cen_pix])
    else:
        ampl = y.max()
    # Return
    return ampl, cent, sigma





def polyfit2d_general(x, y, z, deg, w=None, function='polynomial',
                      minx=None, maxx=None, miny=None, maxy=None):
    """
    :param x: array of x values
    :param y: array of y values
    :param z: value of data at each (x,y) coordinate
    :param deg: degree of polynomial fit in the form [nx,ny]
    :param w: weights
    :return: coefficients
    """
#    msgs.work("Generalize to different polynomial types")
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    deg = np.asarray(deg)
    # Vander
    if function == 'polynomial':
        vander = np.polynomial.polynomial.polyvander2d(x, y, deg)
    elif function == 'legendre':
        xv = scale_minmax(x, minx=minx, maxx=maxx)
        yv = scale_minmax(y, minx=miny, maxx=maxy)
        vander = np.polynomial.legendre.legvander2d(xv, yv, deg)
    else:
        msgs.error("Not ready for this type of {:s}".format(function))
    # Weights
    if w is not None:
        w = np.asarray(w) + 0.0
        if w.ndim != 1:
            msgs.bug("utils.polyfit2d - Expected 1D vector for weights")
        if len(x) != len(w) or len(y) != len(w) or len(x) != len(y):
            msgs.bug("utils.polyfit2d - Expected x, y and weights to have same length")
        z = z * w
        vander = vander * w[:,np.newaxis]
    # Reshape
    vander = vander.reshape((-1,vander.shape[-1]))
    z = z.reshape((vander.shape[0],))
    c = np.linalg.lstsq(vander, z, rcond=None)[0]
    return c.reshape(deg+1)

def scale_minmax(x, minx=None, maxx=None):
    """
    Scale in the input array

    Args:
        x (ndarray): x-values
        minx (float, optional): Minimum value for scaling
        maxx (float, optional): Maximum value for scaling

    Returns:
        ndarray: Scaled x values

    """
    if minx is None or maxx is None:
        if np.size(x) == 1:
            xmin, xmax = -1.0, 1.0
        else:
            xmin, xmax = np.min(x), np.max(x)
    else:
        xmin, xmax = minx, maxx
    xv = 2.0 * (x-xmin)/(xmax-xmin) - 1.0
    return xv




def robust_polyfit(xarray, yarray, order, weights=None, maxone=True, sigma=3.0,
                   function="polynomial", initialmask=None, forceimask=False,
                   minx=None, maxx=None, guesses=None, bspline_par=None, verbose=True):
    """
    A robust (equally weighted) polynomial fit is performed to the xarray, yarray pairs
    mask[i] = 1 are masked values

    :param xarray: independent variable values
    :param yarray: dependent variable values
    :param order: the order of the polynomial to be used in the fitting
    :param weights: weights to be used in the fitting (weights = 1/sigma)
    :param maxone: If True, only the most deviant point in a given iteration will be removed
    :param sigma: confidence interval for rejection
    :param function: which function should be used in the fitting (valid inputs: 'polynomial', 'legendre', 'chebyshev', 'bspline')
    :param initialmask: a mask can be supplied as input, these values will be masked for the first iteration. 1 = value masked
    :param forceimask: if True, the initialmask will be forced for all iterations
    :param minx: minimum value in the array (or the left limit for a legendre/chebyshev polynomial)
    :param maxx: maximum value in the array (or the right limit for a legendre/chebyshev polynomial)
    :return: mask, ct -- mask is an array of the masked values, ct is the coefficients of the robust polyfit.
    """
    # Setup the initial mask
    if initialmask is None:
        mask = np.zeros(xarray.size, dtype=np.int)
        if forceimask:
            msgs.warn("Initial mask cannot be enforced -- no initital mask supplied")
            forceimask = False
    else:
        mask = initialmask.copy()
    mskcnt = np.sum(mask)
    # Iterate, and mask out new values on each iteration
    ct = guesses

    while True:
        w = np.where(mask == 0)
        xfit = xarray[w]
        yfit = yarray[w]
        if weights is not None:
            wfit = weights[w]
        else:
            wfit = None
        ct = func_fit(xfit, yfit, function, order, w=wfit,
                      guesses=ct, minx=minx, maxx=maxx, bspline_par=bspline_par)
        yrng = func_val(ct, xarray, function, minx=minx, maxx=maxx)
        sigmed = 1.4826*np.median(np.abs(yfit-yrng[w]))
        #if xarray.size-np.sum(mask) <= order+2: JFH fixed this bug
        if xarray.size - np.sum(mask) <= order + 1:
            if verbose:
                msgs.warn("More parameters than data points - fit might be undesirable")
            break  # More data was masked than allowed by order
        if maxone:  # Only remove the most deviant point
            tst = np.abs(yarray[w]-yrng[w])
            m = np.argmax(tst)
            if tst[m] > sigma*sigmed:
                mask[w[0][m]] = 1
        else:
            if forceimask:
                w = np.where((np.abs(yarray-yrng) > sigma*sigmed) | (initialmask==1))
            else:
                w = np.where(np.abs(yarray-yrng) > sigma*sigmed)
            mask[w] = 1
        if mskcnt == np.sum(mask): break  # No new values have been included in the mask
        mskcnt = np.sum(mask)

    # Final fit
    w = np.where(mask == 0)
    xfit = xarray[w]
    yfit = yarray[w]
    if weights is not None:
        wfit = weights[w]
    else:
        wfit = None
    ct = func_fit(xfit, yfit, function, order, w=wfit, minx=minx, maxx=maxx, bspline_par=bspline_par)
    return mask, ct

# TODO This should replace robust_polyfit. #ToDO This routine needs to return dicts with the minx and maxx set
def robust_polyfit_djs(xarray, yarray, order, x2 = None, function = 'polynomial', minx = None, maxx = None, minx2 = None, maxx2 = None,
                       bspline_par = None,
                       guesses = None, maxiter=10, inmask=None, sigma=None,invvar=None, lower=None, upper=None,
                       maxdev=None,maxrej=None, groupdim=None,groupsize=None, groupbadpix=False, grow=0,
                       sticky=True, use_mad=True):
    """
    A robust polynomial fit is performed to the xarray, yarray pairs
    mask[i] = 1 are good values

    xarray: independent variable values
    yarray: dependent variable values
    order: the order of the polynomial to be used in the fitting
    x2: ndarray, default = None
       Do a 2d fit?
    function: which function should be used in the fitting (valid inputs: 'polynomial', 'legendre', 'chebyshev', 'bspline')
    minx: minimum value in the array (or the left limit for a legendre/chebyshev polynomial)
    maxx: maximum value in the array (or the right limit for a legendre/chebyshev polynomial)
    guesses : tuple
    bspline_par : dict
        Passed to bspline_fit()
    maxiter : :class:`int`, optional
         Maximum number of rejection iterations, default 10.  Set this to zero to disable rejection and simply do a fit.
    inmask : :class:`numpy.ndarray`, optional
        Input mask.  Bad points are marked with a value that evaluates to ``False``.
        Must have the same number of dimensions as `data`. Points masked as bad "False" in the inmask
        will also always evaluate to "False" in the outmask
    sigma : :class: float or `numpy.ndarray`, optional
        Standard deviation of the yarray, used to reject points based on the values
        of `upper` and `lower`. This can either be a single float for the entire yarray or a ndarray with the same
        shape as the yarray.
    invvar : :class: float or `numpy.ndarray`, optional
        Inverse variance of the data, used to reject points based on the values
        of `upper` and `lower`.  This can either be a single float for the entire yarray or a ndarray with the same
        shape as the yarray. If both `sigma` and `invvar` are set the code will return an error.
    lower : :class:`int` or :class:`float`, optional
        If set, reject points with data < model - lower * sigma.
    upper : :class:`int` or :class:`float`, optional
        If set, reject points with data > model + upper * sigma.
    maxdev : :class:`int` or :class:`float`, optional
        If set, reject points with abs(data-model) > maxdev.  It is permitted to
        set all three of `lower`, `upper` and `maxdev`.
    maxrej: :class:`int` or :class:`numpy.ndarray`, optional
        Maximum number of points to reject in this iteration.  If `groupsize` or
        `groupdim` are set to arrays, this should be an array as well.
    groupdim: class: `int`
        Dimension along which to group the data; set to 1 to group along the 1st dimension, 2 for the 2nd dimension, etc.
        If data has shape [100,200], then setting GROUPDIM=2 is equivalent to grouping the data with groupsize=100.
        In either case, there are 200 groups, specified by [*,i]. NOT WELL TESTED IN PYTHON!
    groupsize: class: `int`
        If this and maxrej are set, then reject a maximum of maxrej points per group of groupsize points.  If groupdim is also
        set, then this specifies sub-groups within that. NOT WELL TESTED IN PYTHON!!
    groupbadpix : :class:`bool`, optional
        If set to ``True``, consecutive sets of bad pixels are considered groups,
        overriding the values of `groupsize`.
    grow : :class:`int`, optional, default = 0
        If set to a non-zero integer, N, the N nearest neighbors of rejected
        pixels will also be rejected.
    sticky : :class:`bool`, optional, default is True
        If set to ``True``, pixels rejected in one iteration remain rejected in
        subsequent iterations, even if the model changes. If
    use_mad : :class: `bool`, optional, defaul = False
        It set to ``True``, compute the median of the maximum absolute deviation between the data and use this for the rejection instead of
        the default which is to compute the standard deviation of the yarray - modelfit. Note that it is not possible to specify use_mad=True
        and also pass in values for sigma or invvar, and the code will return an error if this is done.


    Returns:
    --------
    :return: mask, ct -- mask is an array of the masked values, ct is the coefficients of the robust polyfit.
    """

    # Setup the initial mask
    if inmask is None:
        inmask = np.ones(xarray.size, dtype=bool)

    if sigma is not None and invvar is not None:
        msgs.error('You cannot specify both sigma and invvar')
    elif sigma is not None:
        weights = 1.0/sigma**2
    elif invvar is not None:
        weights = np.copy(invvar)
    else:
        weights = np.ones(xarray.size,dtype=float)

    # Iterate, and mask out new values on each iteration
    ct = guesses

    iIter = 0
    qdone = False
    thismask = np.copy(inmask)
    while (not qdone) and (iIter < maxiter):
        if np.sum(thismask) <= np.sum(order) + 1:
            msgs.warn("More parameters than data points - fit might be undesirable")
        if not np.any(thismask):
            msgs.warn("All points were masked. Returning current fit and masking all points. Fit is likely undesirable")
            if ct is None:
                ct = np.zeros(order + 1)
            return thismask, ct

        ct = func_fit(xarray, yarray, function, order, x2 = x2, w=weights, inmask=thismask,guesses=ct,
                      minx=minx, maxx=maxx,minx2=minx2,maxx2=maxx2, bspline_par=bspline_par)
        ymodel = func_val(ct, xarray, function, x2 = x2, minx=minx, maxx=maxx,minx2=minx2,maxx2=maxx2)
        # TODO Add nrej and nrej_tot as in robust_optimize below?
        thismask, qdone = pydl.djs_reject(yarray, ymodel, outmask=thismask,inmask=inmask, sigma=sigma, invvar=invvar,
                                          lower=lower,upper=upper,maxdev=maxdev,maxrej=maxrej,
                                          groupdim=groupdim,groupsize=groupsize,groupbadpix=groupbadpix,grow=grow,
                                          use_mad=use_mad,sticky=sticky)
        iIter += 1
    if (iIter == maxiter) & (maxiter != 0):
        msgs.warn('Maximum number of iterations maxiter={:}'.format(maxiter) + ' reached in robust_polyfit_djs')
    outmask = np.copy(thismask)
    if np.sum(outmask) == 0:
        msgs.warn('All points were rejected!!! The fits will be zero everywhere.')

    # Do the final fit
    ct = func_fit(xarray, yarray, function, order, x2 = x2, w=weights, inmask = outmask, minx=minx, maxx=maxx, minx2 = minx2, maxx2=maxx2, bspline_par=bspline_par)

    return outmask, ct

def robust_optimize(ydata, fitfunc, arg_dict, maxiter=10, inmask=None, sigma=None,invvar=None, lower=None, upper=None,
                    maxdev=None,maxrej=None, groupdim=None, groupsize=None, groupbadpix=False, grow=0, sticky=True,
                    use_mad=True, **kwargs_optimizer):


    # Setup the initial mask
    if inmask is None:
        inmask = np.ones(ydata.size, dtype=bool)

    if sigma is not None and invvar is not None:
        msgs.error('You cannot specify both sigma and invvar')

    iter = 0
    qdone = False
    thismask = np.copy(inmask)

    while (not qdone) and (iter < maxiter):
        result, ymodel = fitfunc(ydata, thismask, arg_dict, **kwargs_optimizer)
        thismask_iter = thismask.copy()
        thismask, qdone = pydl.djs_reject(ydata, ymodel, outmask=thismask, inmask=inmask, invvar=invvar,
                                          lower=lower, upper=upper, maxdev=maxdev, maxrej=maxrej,
                                          groupdim=groupdim, groupsize=groupsize, groupbadpix=groupbadpix, grow=grow,
                                          use_mad=use_mad, sticky=sticky)
        nrej = np.sum(thismask_iter & np.invert(thismask))
        nrej_tot = np.sum(inmask & np.invert(thismask))
        msgs.info(
            'Iteration #{:d}: nrej={:d} new rejections, nrej_tot={:d} total rejections'.format(iter, nrej, nrej_tot))
        iter += 1

    if (iter == maxiter) & (maxiter != 0):
        msgs.warn('Maximum number of iterations maxiter={:}'.format(maxiter) + ' reached in sens_tell_fit')
    outmask = np.copy(thismask)
    if np.sum(outmask) == 0:
        msgs.warn('All points were rejected!!! The fits will be zero everywhere.')

    # Perform a final fit using the final outmask
    result, ymodel = fitfunc(ydata, outmask, arg_dict, **kwargs_optimizer)

    return result, ymodel, outmask

def subsample(frame):
    """
    Used by LACosmic

    Args:
        frame (ndarray):

    Returns:
        ndarray: Sliced image

    """
    newshape = (2*frame.shape[0], 2*frame.shape[1])
    slices = [slice(0, old, float(old)/new) for old, new in zip(frame.shape, newshape)]
    coordinates = np.mgrid[slices]
    indices = coordinates.astype('i')
    return frame[tuple(indices)]



def yamlify(obj, debug=False):
    """Recursively process an object so it can be serialised for yaml.
    Based on jsonify in `linetools <https://pypi.python.org/pypi/linetools>`_.

    Note: All string-like keys in :class:`dict` s are converted to
    :class:`str`.

    Also found in desiutils

    Parameters
    ----------
    obj : :class:`object`
        Any object.
    debug : :class:`bool`, optional
        Print extra information if requested.

    Returns
    -------
    :class:`object`
       An object suitable for yaml serialization.  For example
       :class:`numpy.ndarray` is converted to :class:`list`,
       :class:`numpy.int64` is converted to :class:`int`, etc.
    """
    if isinstance(obj, (np.float64, np.float32)):
        obj = float(obj)
    elif isinstance(obj, (np.int32, np.int64, np.int16)):
        obj = int(obj)
    elif isinstance(obj, np.bool_):
        obj = bool(obj)
#    elif isinstance(obj, bytes):
#        obj = obj.decode('utf-8')
    elif isinstance(obj, (np.string_, str)):
        obj = str(obj)
    elif isinstance(obj, units.Quantity):
        try:
            obj = obj.value.tolist()
        except AttributeError:
            obj = obj.value
    elif isinstance(obj, np.ndarray):  # Must come after Quantity
        obj = obj.tolist()
    elif isinstance(obj, dict):
        # First convert keys
        nobj = {}
        for key, value in obj.items():
            if isinstance(key, str):
                nobj[str(key)] = value
            else:
                nobj[key] = value
        # Now recursive
        obj = nobj
        for key, value in obj.items():
            obj[key] = yamlify(value, debug=debug)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            obj[i] = yamlify(item, debug=debug)
    elif isinstance(obj, tuple):
        obj = list(obj)
        for i, item in enumerate(obj):
            obj[i] = yamlify(item, debug=debug)
        obj = tuple(obj)
    # elif isinstance(obj, Unit):
    #     obj = obj.name
    # elif obj is units.dimensionless_unscaled:
    #     obj = 'dimensionless_unit'
    if debug:
        print(type(obj))
    return obj


