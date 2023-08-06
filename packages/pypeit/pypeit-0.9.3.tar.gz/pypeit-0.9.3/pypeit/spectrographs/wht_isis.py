""" Module for Shane/Kast specific codes
"""
from __future__ import absolute_import, division, print_function

import numpy as np

from astropy.io import fits

from pypeit import msgs
from pypeit import telescopes
from pypeit.core import framematch
from pypeit.par import pypeitpar
from pypeit.spectrographs import spectrograph
from pypeit.core import parse

from pypeit import debugger

#class WhtIsisSpectrograph(spectrograph.Spectrograph):
#    """
#    Child to handle Shane/Kast specific code
#    """
#
#    def __init__(self):
#        super(WhtIsisSpectrograph, self).__init__()
#        self.spectrograph = 'wht_isis_base'
#        self.telescope = telescopes.WHTTelescopePar()
#
#    def metadata_keys(self):
#        return super(KeckLRISSpectrograph, self).metadata_keys() \
#                    + ['binning', 'dichroic', 'dispangle']

# TODO: Change this to WHTISISBlueSpectrograph
class WhtIsisBlueSpectrograph(spectrograph.Spectrograph):
    """
    Child to handle WHT/ISIS blue specific code
    """
    def __init__(self):
        # Get it started
        super(WhtIsisBlueSpectrograph, self).__init__()
        self.spectrograph = 'wht_isis_blue'
        self.telescope = telescopes.WHTTelescopePar()
        self.camera = 'ISISb'
        self.detector = [
                # Detector 1
                pypeitpar.DetectorPar(
                            dataext         = 1,
                            specaxis        = 0,
                            specflip        = False,
                            xgap            = 0.,
                            ygap            = 0.,
                            ysize           = 1.,
                            platescale      = 0.225,
                            darkcurr        = 0.0,
                            saturation      = 65535.,
                            nonlinear       = 0.76,
                            numamplifiers   = 1,
                            gain            = 1.2,
                            ronoise         = 5.0,
                            datasec         = '[:,2:4030]',
                            # TODO: What happens when the overscan is
                            # not defined?!
                            oscansec        = '[:,:]',
                            suffix          = '_blue'
                            )]
        self.numhead = 2
        # Uses default timeunit
        # Uses default primary_hdrext
        # self.sky_file = ?

    @staticmethod
    def default_pypeit_par():
        """
        Set default parameters for Keck LRISb reductions.
        """
        par = pypeitpar.PypeItPar()
        par['rdx']['spectrograph'] = 'wht_isis_blue'
        # Set pixel flat combination method
        par['calibrations']['pixelflatframe']['process']['combine'] = 'median'
        par['calibrations']['pixelflatframe']['process']['sig_lohi'] = [10.,10.]
        # Change the wavelength calibration method
        par['calibrations']['wavelengths']['method'] = 'simple'
        # Scienceimage default parameters
        par['scienceimage'] = pypeitpar.ScienceImagePar()
        # Do not flux calibrate
        par['fluxcalib'] = None
        # Always correct for flexure, starting with default parameters
        par['flexure'] = pypeitpar.FlexurePar()
        # Set the default exposure time ranges for the frame typing
        par['calibrations']['biasframe']['exprng'] = [None, 1]
        par['calibrations']['darkframe']['exprng'] = [999999, None]     # No dark frames
        par['calibrations']['pinholeframe']['exprng'] = [999999, None]  # No pinhole frames
        par['calibrations']['arcframe']['exprng'] = [None, 120]
        par['calibrations']['standardframe']['exprng'] = [None, 120]
        par['scienceframe']['exprng'] = [90, None]
        return par

    def init_meta(self):
        """
        Generate the meta data dict
        Note that the children can add to this

        Returns:
            self.meta: dict (generated in place)

        """
        meta = {}
        # Required (core)
        meta['ra'] = dict(ext=0, card='RA')
        meta['dec'] = dict(ext=0, card='DEC')
        meta['target'] = dict(ext=0, card='OBJECT')
        meta['decker'] = dict(card=None, compound=True)
        meta['binning'] = dict(card=None, compound=True)

        meta['mjd'] = dict(ext=0, card='MJD-OBS')
        meta['exptime'] = dict(ext=0, card='EXPTIME')
        meta['airmass'] = dict(ext=0, card='AIRMASS')
        meta['decker'] = dict(ext=0, card='ISISLITU')
        # Extras for config and frametyping
        meta['dispname'] = dict(ext=0, card='ISIGRAT')
        meta['dichroic'] = dict(ext=0, card='ISIDICHR')
        meta['dispangle'] = dict(ext=0, card='CENWAVE', rtol=1e-4)
        meta['slitwid'] = dict(ext=0, card='ISISLITW')
        meta['idname'] = dict(ext=0, card='IMAGETYP')
        # Lamps
        meta['lampstat01'] = dict(ext=0, card='CAGLAMPS')

        # Ingest
        self.meta = meta

    def compound_meta(self, headarr, meta_key):
        if meta_key == 'binning':
            binspatial = headarr[0]['CCDXBIN']
            binspec = headarr[0]['CCDYBIN']
            return parse.binning2string(binspec, binspatial)
        else:
            msgs.error("Not ready for this compound meta")

    def configuration_keys(self):
        """
        Return the metadata keys that defines a unique instrument
        configuration.

        This list is used by :class:`pypeit.metadata.PypeItMetaData` to
        identify the unique configurations among the list of frames read
        for a given reduction.

        Returns:
            list: List of keywords of data pulled from meta
        """
        return ['dispname', 'decker', 'binning', 'dispangle', 'dichroic']

    def pypeit_file_keys(self):
        pypeit_keys = super(WhtIsisBlueSpectrograph, self).pypeit_file_keys()
        pypeit_keys += ['slitwid']
        return pypeit_keys

    def check_frame_type(self, ftype, fitstbl, exprng=None):
        """
        Check for frames of the provided type.
        """
        good_exp = framematch.check_frame_exptime(fitstbl['exptime'], exprng)
        if ftype in ['science', 'standard']:
            return good_exp & (fitstbl['lampstat01'] == 'Off') & (fitstbl['idname'] == 'object')
        if ftype == 'bias':
            return good_exp & (fitstbl['idname'] == 'zero')
        if ftype in ['pixelflat', 'trace']:
            return good_exp & (fitstbl['lampstat01'] == 'W') & (fitstbl['idname'] == 'flat')
        if ftype in ['pinhole', 'dark']:
            # Don't type pinhole or dark frames
            return np.zeros(len(fitstbl), dtype=bool)
        if ftype == 'arc':
            return good_exp & (fitstbl['lampstat01'] == 'CuNe+CuAr') & (fitstbl['idname'] == 'arc')
        msgs.warn('Cannot determine if frames are of type {0}.'.format(ftype))
        return np.zeros(len(fitstbl), dtype=bool)

#    def parse_binning(self, inp, det=1):
#        """
#        Get the pixel binning for an image.
#
#        Args:
#            inp (:obj:`str`, `astropy.io.fits.Header`):
#                String providing the file name to read, or the relevant
#                header object.
#            det (:obj:`int`, optional):
#                1-indexed detector number.
#
#        Returns:
#            str: String representation of the binning.  The ordering is
#            as provided in the header, regardless of which axis is
#            designated as the dispersion axis.  It is expected that this
#            be used with :func:`pypeit.core.parse.sec2slice` to setup
#            the data and overscane sections of the image data.
#
#        Raises:
#            PypeItError:
#                Raised if `inp` is not one of the accepted types.
#        """
#        # Get the header
#        # TODO: Read primary header by default instead?
#        if isinstance(inp, str):
#            hdu = fits.open(inp)
#            hdr = hdu[self.detector[det-1]['dataext']].header
#        elif isinstance(inp, fits.Header):
#            hdr = inp
#        else:
#            msgs.error('Input must be a filename or fits.Header object')
#
#        return parse.binning2string(hdr['CCDXBIN'], hdr['CCDYBIN'])

#    def get_match_criteria(self):
#        match_criteria = {}
#        for key in framematch.FrameTypeBitMask().keys():
#            match_criteria[key] = {}
#        # Standard
#        match_criteria['standard']['match'] = {}
#        match_criteria['standard']['match']['naxis0'] = '=0'
#        match_criteria['standard']['match']['naxis1'] = '=0'
##        match_criteria['standard']['match']['decker'] = ''
##        match_criteria['standard']['match']['dispangle'] = '|<=1'
#        # Bias
#        match_criteria['bias']['match'] = {}
#        match_criteria['bias']['match']['naxis0'] = '=0'
#        match_criteria['bias']['match']['naxis1'] = '=0'
#        # Pixelflat
#        match_criteria['pixelflat']['match'] = {}
#        match_criteria['pixelflat']['match']['naxis0'] = '=0'
#        match_criteria['pixelflat']['match']['naxis1'] = '=0'
#        match_criteria['pixelflat']['match']['decker'] = ''
#        match_criteria['pixelflat']['match']['dispangle'] = '|<=1'
#        # Traceflat
#        match_criteria['trace']['match'] = match_criteria['pixelflat']['match'].copy()
#        # Arc
#        match_criteria['arc']['match'] = {}
#        match_criteria['arc']['match']['naxis0'] = '=0'
#        match_criteria['arc']['match']['naxis1'] = '=0'
#        match_criteria['arc']['match']['dispangle'] = '|<=1'
#
#        return match_criteria
#
#    def setup_arcparam(self, arcparam, disperser=None, fitstbl=None,
#                       arc_idx=None, msarc_shape=None, **null_kwargs):
#        """
#        Setup the arc parameters
#
#        Args:
#            arcparam: dict
#            disperser: str, REQUIRED
#            **null_kwargs:
#              Captured and never used
#
#        Returns:
#            arcparam is modified in place
#            modify_dict: dict
#
#        """
#        modify_dict = dict(NeI={'min_wave': 3000.,'min_intensity': 299,
#                                'min_Aki': 0.},ArI={'min_intensity': 399.})
#        arcparam['lamps']=['CuI','NeI','ArI']
#        arcparam['nonlinear_counts'] = self.detector[0]['nonlinear']*self.detector[0]['saturation']
#
#        if fitstbl["dichroic"][arc_idx].strip() == '5300':
#            arcparam['wvmnx'][1] = 6000.
#        else:
#            msgs.error('Not ready for this dichroic {:s}!'.format(disperser))
#        if disperser == 'R300B':
#            arcparam['n_first']=1  #
#            arcparam['disp']=0.80  # Ang per pixel (unbinned)
#            arcparam['b1']= 1./arcparam['disp']/msarc_shape[0]
#        else:
#            msgs.error('Not ready for this disperser {:s}!'.format(disperser))
#        #
#        return modify_dict

