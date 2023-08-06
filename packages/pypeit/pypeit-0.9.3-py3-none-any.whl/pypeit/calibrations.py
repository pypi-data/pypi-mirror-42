""" Class for guiding calibration object generation in PypeIt
"""
from __future__ import absolute_import, division, print_function

import os
import numpy as np

from abc import ABCMeta

from astropy.table import Table

from pypeit import msgs
from pypeit.core import pixels
from pypeit import masterframe
from pypeit import arcimage
from pypeit import biasframe
#from pypeit import bpmimage
from pypeit import flatfield
from pypeit import traceimage
from pypeit import traceslits
from pypeit import wavecalib
from pypeit import wavetilts
from pypeit import waveimage

from pypeit.metadata import PypeItMetaData

from pypeit.core import procimg
from pypeit.core import parse
from pypeit.core import trace_slits

from pypeit.par import pypeitpar
from pypeit.spectrographs.util import load_spectrograph

from pypeit import debugger


class Calibrations(object):
    """
    This class is primarily designed to guide the generation of
    calibration images and objects in PypeIt.

    To avoid rebuilding MasterFrames that were generated during this execution
    of PypeIt, the class performs book-keeping of these master frames and
    holds that info in self.calib_dict

    Args:
        fitstbl (:class:`pypeit.metadata.PypeItMetaData`):
            The class holding the metadata for all the frames in this
            PypeIt run.
        par (:class:`pypeit.par.pypeitpar.PypeItPar`):
            Parameter set defining optional parameters of PypeIt's
            low-level algorithms.  Needs to specifically be a
            CalibrationsPar child.
        spectrograph (:obj:`pypeit.spectrographs.spectrograph.Spectrograph`):
            Spectrograph object
        redux_path (:obj:`str`, optional):
            Top-level directory for PypeIt output.  If None, the current
            working directory is used.
        reuse_masters (:obj:`bool`, optional):
            Load calibration files from disk if they exist
        save_masters (:obj:`bool`, optional):
            Save calibration files to disk (should always be True)
        write_qa (:obj:`bool`, optional):
            Create QA plots.
        show (:obj:`bool`, optional):
            Show plots of PypeIt's results as the code progesses.
            Requires interaction from the users.

    Attributes:
        fitstbl
        save_masters
        write_qa
        show
        spectrograph
        par
        redux_path
        master_dir
        calib_dict
        det
        frame (:obj:`int`):
            0-indexed row of the frame being calibrated in
            :attr:`fitstbl`.
        calib_ID (:obj:`int`):
            calib group ID of the current frame
        arc_master_key

    """
    __metaclass__ = ABCMeta

    def __init__(self, fitstbl, par, spectrograph, redux_path=None, reuse_masters=False, save_masters=True,
                 write_qa=True, show=False):

        # Check the type of the provided fits table
        if not isinstance(fitstbl, PypeItMetaData):
            msgs.error('fitstbl must be an PypeItMetaData object')

        # Parameters unique to this Object
        self.fitstbl = fitstbl
        self.save_masters = save_masters
        self.reuse_masters = reuse_masters
        self.write_qa = write_qa
        self.show = show

        # Test par
        self.par = par
        if not isinstance(self.par, pypeitpar.CalibrationsPar):
            raise TypeError('Input parameters must be a CalibrationsPar instance.')

        # Spectrometer class
        self.spectrograph = spectrograph

        # Output dirs
        self.redux_path = os.getcwd() if redux_path is None else redux_path
        self.master_dir = masterframe.set_master_dir(self.redux_path, self.spectrograph, self.par)

        # Attributes
        self.calib_dict = {}
        self.det = None
        self.frame = None
        self.binning = None
        self.calib_ID = None
        self.master_key_dict = {}

        # Steps
        self.steps = []

        # Internals
        self._reset_internals()

    def _reset_internals(self):
        """
        Reset all of the key internals to None or an empty object

        """
        self.shape = None
        self.msarc = None
        self.msbias = None
        self.msbpm = None
        self.tslits_dict = None
        self.maskslits = None
        self.wavecalib = None
        self.tilts_dict = None
        self.mspixflatnrm = None
        self.msillumflat = None
        self.mswave = None
        self.cailb_ID = None
        self.master_key_dict = {}

    def check_for_previous(self, ftype, master_key):
        """
        Check to see whether the master file(s) have been
        built during this run of PypeIt.
        If so, we will likely either load from memory or hard-drive

        calib_dict is nested as:
           [master_key][ftype]

        If the ftype has not yet been generated, an empty dict is prepared
           self.calib_dict[master_key][ftype] = {}

        Args:
            ftype (str): Type of calibration frame
            master_key (str): Master key naming

        Returns:
             bool: True = Built previously
        """
        previous = False
        if master_key in self.calib_dict.keys():
            if ftype in self.calib_dict[master_key].keys():
                previous = True
        else:  # Prep for saving
            self.calib_dict[master_key] = {}
        # Return
        return previous

    def set_config(self, frame, det, par=None):
        """
        Specify the parameters of the Calibrations class and reset all
        the internals to None. The internal dict is left unmodified.

        Args:
            frame (int): Frame index in the fitstbl
            det (int): Detector number
            par (:class:`pypeit.par.pypeitpar.CalibrationPar`):

        """
        self.frame = frame
        self.calib_ID = int(self.fitstbl['calib'][frame])
        self.det = det
        if par is not None:
            self.par = par
        # Deal with binning
        self.binning = self.fitstbl['binning'][self.frame]

        # Reset internals to None
        self._reset_internals()
        # Initialize the master key dict for this science/standard frame
        self.master_key_dict['frame'] = self.fitstbl.master_key(frame, det=det)

    def get_arc(self):
        """
        Load or generate the Arc image

        Requirements:
          master_key, det, par

        Args:

        Returns:
            ndarray: :attr:`msarc` image

        """
        # Check internals
        self._chk_set(['det', 'calib_ID', 'par'])

        # Prep
        arc_rows = self.fitstbl.find_frames('arc', calib_ID=self.calib_ID, index=True)
        self.arc_files = self.fitstbl.frame_paths(arc_rows)
        self.arc_master_key = self.fitstbl.master_key(arc_rows[0], det=self.det)
        self.master_key_dict['arc'] = self.arc_master_key

        prev_build = self.check_for_previous('arc', self.arc_master_key)
        if prev_build:
            # Previously calculated
            self.msarc = self.calib_dict[self.arc_master_key]['arc']
            return self.msarc

        # Instantiate with everything needed to generate the image (in case we do)
        self.arcImage = arcimage.ArcImage(self.spectrograph, files=self.arc_files,
                                          det=self.det, msbias=self.msbias,
                                          par=self.par['arcframe'], master_key=self.arc_master_key,
                                          master_dir=self.master_dir, reuse_masters=self.reuse_masters)

        # Load the MasterFrame (if it exists and is desired)?
        self.msarc, _ = self.arcImage.master(prev_build=prev_build)
        if self.msarc is None:  # Otherwise build it
            msgs.info("Preparing a master {0:s} frame".format(self.arcImage.frametype))
            self.msarc = self.arcImage.build_image()
            # Save to Masters
            if self.save_masters:
                self.arcImage.save_master(self.msarc, raw_files=self.arcImage.files,
                                          steps=self.arcImage.steps)

        # Save & return
        self.calib_dict[self.arc_master_key]['arc'] = self.msarc
        return self.msarc

    def get_bias(self):
        """
        Load or generate the bias frame/command

        Requirements:
           master_key, det, par

        Returns:
            ndarray or str: :attr:`bias`

        """

        # Check internals
        self._chk_set(['det', 'calib_ID', 'par'])

        # Prep
        bias_rows = self.fitstbl.find_frames('bias', calib_ID=self.calib_ID, index=True)
        self.bias_files = self.fitstbl.frame_paths(bias_rows)
        if len(bias_rows) > 0:
            self.bias_master_key = self.fitstbl.master_key(bias_rows[0], det=self.det)
        else:  # Allow for other bias modes
            self.bias_master_key = self.fitstbl.master_key(self.frame, det=self.det)
        self.master_key_dict['bias'] = self.bias_master_key

        # Grab from internal dict (or hard-drive)?
        prev_build = self.check_for_previous('bias', self.bias_master_key)
        if prev_build:
            self.msbias = self.calib_dict[self.bias_master_key]['bias']
            msgs.info("Reloading the bias from the internal dict")
            return self.msbias

        # Instantiate
        self.biasFrame = biasframe.BiasFrame(self.spectrograph, files=self.bias_files,
                                             det=self.det, par=self.par['biasframe'],
                                             master_key=self.bias_master_key,
                                             master_dir=self.master_dir, reuse_masters=self.reuse_masters)

        # How are we treating biases: 1) No bias, 2) overscan, or 3) use
        # bias subtraction. If use bias is there a master?
        self.msbias = self.biasFrame.determine_bias_mode(prev_build=prev_build)
        # This could be made more elegant, like maybe msbias should be
        # set to 'none' analgous to how overscan is treated???
        if (self.msbias is None) and (self.par['biasframe']['useframe'] != 'none'):
            # Build it and save it
            self.msbias = self.biasFrame.build_image()
            if self.save_masters:
                self.biasFrame.save_master(self.msbias, raw_files=self.biasFrame.files,
                                           steps=self.biasFrame.steps)

        # Save & return
        self.calib_dict[self.bias_master_key]['bias'] = self.msbias
        return self.msbias

    def get_bpm(self):
        """
        Load or generate the bad pixel mask

        TODO -- Should consider doing this outside of calibrations as it is
        more specific to the science frame

        This needs to be for the *trimmed* image!

        Requirements:
           Instrument dependent

        Returns:
            ndarray: :attr:`msbpm` image of bad pixel mask

        """
        # Check internals
        self._chk_set(['par', 'det'])

        # Generate a bad pixel mask (should not repeat)
        self.bpm_master_key = self.fitstbl.master_key(self.frame, det=self.det)
        self.master_key_dict['bpm'] = self.bpm_master_key

        prev_build = self.check_for_previous('bpm', self.bpm_master_key)
        if prev_build:
            self.msbpm = self.calib_dict[self.bpm_master_key]['bpm']
            return self.msbpm

        # Always use the shape!
        #  But some instruments need the filename too, e.g. for binning
        sci_image_files = [self.fitstbl.frame_paths(self.frame)]
        # TODO JFH These lines below should either go into the spectrograph class or to the BPM image class, they
        # do not belong here.
        dsec_img = self.spectrograph.get_datasec_img(sci_image_files[0], det=self.det)
        # Instantiate the shape here, based on the shape of the science image. This is the shape of most
        # most calibrations, although we are allowing for arcs of different shape becuase of X-shooter etc.
        self.shape = procimg.trim_frame(dsec_img, dsec_img < 1).shape

        # Build it
        self.msbpm = self.spectrograph.bpm(shape=self.shape, filename=sci_image_files[0], det=self.det)
        # Record it
        self.calib_dict[self.bpm_master_key]['bpm'] = self.msbpm
        # Return
        return self.msbpm

    def get_flats(self):
        """
        Load or generate a normalized pixel flat
          and slit profile

        Requirements:
           tslits_dict
           tilts_dict
           det, par

        Returns:
            ndarray, ndarray: :attr:`mspixflatnrm` which is the normalized pixel flat image
            and :attr:`msillumflat` which is the illumination flat.

        """

        if self.par['flatfield']['method'] is 'skip':
            # User does not want to flat-field
            self.mspixflatnrm = None
            self.msillumflat = None
            msgs.warning('Parameter calibrations.flatfield.method is set to skip. You are NOT '
                         'flatfielding your data!!!')
            return self.mspixflatnrm, self.msillumflat

        # Check for existing data necessary to build flats
        if not self._chk_objs(['tslits_dict', 'tilts_dict']):
            msgs.warning('Flats were requested, but there are quantities missing necessary to '
                         'create flats.  Proceeding without flat fielding....')
            # User cannot flat-field
            self.mspixflatnrm = None
            self.msillumflat = None
            return self.mspixflatnrm, self.msillumflat

        # Check internals
        self._chk_set(['det', 'calib_ID', 'par'])

        pixflat_rows = self.fitstbl.find_frames('pixelflat', calib_ID=self.calib_ID, index=True)
        # TODO: Why aren't these set to self
        pixflat_image_files = self.fitstbl.frame_paths(pixflat_rows)
        if len(pixflat_rows) > 0:
            self.pixflat_master_key = self.fitstbl.master_key(pixflat_rows[0], det=self.det)
        else:  # Allow for user-supplied file (e.g. LRISb)
            self.pixflat_master_key = self.fitstbl.master_key(self.frame, det=self.det)

        self.master_key_dict['flat'] = self.pixflat_master_key
        # Return already generated data
        prev_build1 = self.check_for_previous('normpixelflat', self.pixflat_master_key)
        prev_build2 = self.check_for_previous('illumflat', self.pixflat_master_key)
        if np.all([prev_build1, prev_build2]):
            self.mspixflatnrm = self.calib_dict[self.pixflat_master_key]['normpixelflat']
            self.msillumflat = self.calib_dict[self.pixflat_master_key]['illumflat']
            return self.mspixflatnrm, self.msillumflat

        # Instantiate
        self.flatField = flatfield.FlatField(self.spectrograph,
                                             self.par['pixelflatframe'],
                                             files=pixflat_image_files,
                                             det=self.det,
                                             master_key=self.pixflat_master_key, master_dir=self.master_dir,
                                             reuse_masters=self.reuse_masters,
                                             flatpar=self.par['flatfield'], msbias=self.msbias,
                                             tslits_dict=self.tslits_dict,
                                             tilts_dict=self.tilts_dict)

        # --- Pixel flats

        # 1)  Try to load master files from disk (MasterFrame)?
        self.mspixflatnrm, _  = self.flatField.master(prev_build=prev_build1)
        if prev_build2:
            self.msillumflat, _ = self.flatField.load_master_illumflat()

        # 2) Did the user specify a flat? If so load it in  (e.g. LRISb with pixel flat)?
        if self.par['flatfield']['frame'] not in ['pixelflat']:
            # First try to find directly, then try to find it in the
            # masters directory, then fail
            if os.path.isfile(self.par['flatfield']['frame']):
                mspixelflat_name = self.par['flatfield']['frame']
            elif os.path.isfile(os.path.join(self.flatField.directory_path,
                                             self.par['flatfield']['frame'])):
                mspixelflat_name = os.path.join(self.flatField.directory_path,
                                                self.par['flatfield']['frame'])
            else:
                raise ValueError('Could not find user-defined flatfield master: {0}'.format(
                    self.par['flatfield']['frame']))
            msgs.info('Found user-defined file: {0}'.format(mspixelflat_name))
            self.mspixflatnrm, _ = self.flatField.load_master(mspixelflat_name, exten=self.det)

        # 3) there is no master or no user supplied flat, generate the flat
        if self.mspixflatnrm is None and len(pixflat_image_files) != 0:
            # Run
            self.mspixflatnrm, self.msillumflat = self.flatField.run(show=self.show)

            # If we tweaked the slits, update the tilts_dict and
            # tslits_dict to reflect new slit edges
            if self.par['flatfield']['tweak_slits']:
                msgs.info('Using slit boundary tweaks from IllumFlat and updated tilts image')
                self.tslits_dict = self.flatField.tslits_dict
                self.tilts_dict = self.flatField.tilts_dict

            # Save to Masters
            if self.save_masters:
                self.flatField.save_master(self.mspixflatnrm, raw_files=pixflat_image_files,
                                           steps=self.flatField.steps)
                if self.msillumflat is not None:
                    self.flatField.save_master(self.msillumflat, raw_files=pixflat_image_files,
                                               steps=self.flatField.steps,
                                               outfile=masterframe.master_name('illumflat',
                                               self.pixflat_master_key,self.master_dir))
                # If we tweaked the slits update the master files for tilts and slits
                if self.par['flatfield']['tweak_slits']:
                    msgs.info('Updating MasterTrace and MasterTilts using tweaked slit boundaries')
                    # Add tweaked boundaries to the MasterTrace file
                    self.traceSlits.save_master(self.flatField.tslits_dict)
                    # Write the final_tilts using the new slit boundaries to the MasterTilts file
                    self.waveTilts.final_tilts = self.flatField.tilts_dict['tilts']
                    self.waveTilts.tilts_dict = self.flatField.tilts_dict
                    self.waveTilts.save_master(self.flatField.tilts_dict, steps=self.waveTilts.steps)

        # 4) If we still don't have a pixel flat, then just use unity
        # everywhere and print out a warning
        if self.mspixflatnrm is None:
            self.mspixflatnrm = np.ones_like(self.tilts_dict['tilts'])
            msgs.warn('You are not pixel flat fielding your data!!!')

        # --- Illumination flats

        # 1) If we ran the flat field algorithm above, then the
        # illumination file was created. So check msillumflat is set
        if self.msillumflat is None:
            # 2) If no illumination file is set yet, try to read it in from a master
            self.msillumflat, _ = self.flatField.load_master_illumflat()
            # 3) If there is no master file, then set illumflat to unit
            # and war user that they are not illumflatting their data
            if self.msillumflat is None:
                self.msillumflat = np.ones_like(self.tilts_dict['tilts'])
                msgs.warn('You are not illumination flat fielding your data!')

        # Save & return
        self.calib_dict[self.pixflat_master_key]['normpixelflat'] = self.mspixflatnrm
        self.calib_dict[self.pixflat_master_key]['illumflat'] = self.msillumflat

        return self.mspixflatnrm, self.msillumflat

    def get_slits(self, redo=False, write_qa=True):
        """
        Load or generate the slits.
        First, a trace flat image is generated

        Requirements:
           det, par, master_key

        Args:
            redo (bool): Redo
            write_qa: bool, optional
              Generate the QA?  Turn off for testing..

        Returns:
            dict, ndarray: :attr:`tslits_dict` trace slits dict and :attr:`maskslits` array
            of slit mask

        """
        # Check for existing data
        if not self._chk_objs(['msbpm']):
            self.tslits_dict = None
            self.maskslits = None
            return self.tslits_dict, self.maskslits

        # Check internals
        self._chk_set(['det', 'calib_ID', 'par'])

        # Prep
        trace_rows = self.fitstbl.find_frames('trace', calib_ID=self.calib_ID, index=True)
        self.trace_image_files = self.fitstbl.frame_paths(trace_rows)

        self.trace_master_key = self.fitstbl.master_key(trace_rows[0], det=self.det)
        self.master_key_dict['trace'] = self.trace_master_key

        # Return already generated data
        prev_build = self.check_for_previous('trace', self.trace_master_key)
        if prev_build and (not redo):
            self.tslits_dict = self.calib_dict[self.trace_master_key]['trace']
            self.maskslits = np.zeros(self.tslits_dict['slit_left'].shape[1], dtype=bool)
            return self.tslits_dict, self.maskslits

        # Instantiate (without mstrace)
        self.traceSlits = traceslits.TraceSlits(None, self.spectrograph, self.par['slits'],
                                                binning=self.binning,
                                                det=self.det, master_key=self.trace_master_key,
                                                master_dir=self.master_dir,
                                                redux_path=self.redux_path,
                                                reuse_masters=self.reuse_masters,
                                                msbpm=self.msbpm)

        # Load via master, as desired
        self.tslits_dict, _ = self.traceSlits.master(prev_build=prev_build)
        if self.tslits_dict is None:
            # Build the trace image first
            self.traceImage = traceimage.TraceImage(self.spectrograph,self.trace_image_files, det=self.det,
                                           par=self.par['traceframe'])
            # Load up and get ready
            self.traceSlits.mstrace = self.traceImage.process(bias_subtract=self.msbias,
                                                         trim=self.par['trim'], apply_gain=True)

            # Compute the plate scale in arcsec which is needed to trim short slits
            binspectral, binspatial = parse.parse_binning(self.binning)
            plate_scale = binspatial*self.spectrograph.detector[self.det-1]['platescale']

            # JFH Why is this stuff on user defined slits here and not in the class?
            # User-defined slits??
            add_user_slits = trace_slits.parse_user_slits(self.par['slits']['add_slits'], self.det)
            rm_user_slits = trace_slits.parse_user_slits(self.par['slits']['rm_slits'], self.det, rm=True)
            # Now we go forth
            try:
                self.tslits_dict = self.traceSlits.run(plate_scale=plate_scale, show=self.show,
                                                       add_user_slits=add_user_slits, rm_user_slits=rm_user_slits,
                                                       write_qa=write_qa)
            except:
                self.traceSlits.save_master(self.tslits_dict)
                msgs.error("Crashed out of finding the slits. Have saved the work done to disk but it needs fixing..")
            # No slits?
            if self.tslits_dict is None:
                self.maskslits = None
                return self.tslits_dict, self.maskslits
            # Save to disk
            if self.save_masters:
                # Master
                self.traceSlits.save_master(self.tslits_dict)
        else:
            msgs.info("TraceSlits master files loaded..")
            # Construct dictionary
            #self.tslits_dict = self.traceSlits._fill_tslits_dict()

        # Save, initialize maskslits, and return
        self.calib_dict[self.trace_master_key]['trace'] = self.tslits_dict
        self.maskslits = np.zeros(self.tslits_dict['slit_left'].shape[1], dtype=bool)

        return self.tslits_dict, self.maskslits

    def get_wave(self):
        """
        Load or generate a wavelength image

        Requirements:
           tilts_dict, tslits_dict, wv_calib, maskslits
           det, par, master_key

        Returns:
            ndarray: :attr:`mswave` wavelength image

        """
        # Check for existing data
        if not self._chk_objs(['tilts_dict','tslits_dict','wv_calib','maskslits']):
            self.mswave = None
            return self.mswave

        # Check internals
        self._chk_set(['arc_master_key', 'det', 'par'])

        # Return existing data
        prev_build = self.check_for_previous('wave', self.arc_master_key)
        if prev_build:
            self.mswave = self.calib_dict[self.arc_master_key]['wave']
            return self.mswave

        # No wavelength calibration requested
        if self.par['wavelengths']['reference'] == 'pixel':
            self.mswave = self.tilts_dict['tilts'] * (self.tilts_dict['tilts'].shape[0]-1.0)
            self.calib_dict[self.arc_master_key]['wave'] = self.mswave
            return self.mswave

        # Instantiate
        # ToDO we are regenerating this mask a lot in this module. Could reduce that
        self.waveImage = waveimage.WaveImage(self.tslits_dict, self.tilts_dict['tilts'], self.wv_calib,
                                             self.spectrograph, self.maskslits,
                                             master_key=self.arc_master_key, master_dir=self.master_dir,
                                             reuse_masters=self.reuse_masters)
        # Attempt to load master
        self.mswave, _  = self.waveImage.master(prev_build=prev_build)
        if self.mswave is None:
            self.mswave = self.waveImage._build_wave()
        # Save to hard-drive
        if self.save_masters:
            self.waveImage.save_master(self.mswave, steps=self.waveImage.steps)

        # Save & return
        self.calib_dict[self.arc_master_key]['wave'] = self.mswave

        return self.mswave

    def get_wv_calib(self):
        """
        Load or generate the 1D wavelength calibrations

        Requirements:
          msarc, msbpm, tslits_dict, maskslits
          det, par, arc_master_key

        Returns:
            dict, ndarray: :attr:`wv_calib` calibration dict and the updated slit mask array
        """
        # Check for existing data
        if not self._chk_objs(['msarc', 'msbpm', 'tslits_dict', 'maskslits']):
            msgs.error('dont have all the objects')

        # Check internals
        self._chk_set(['arc_master_key', 'det', 'calib_ID', 'par'])

        # Return existing data
        prev_build = self.check_for_previous('wavecalib', self.arc_master_key)
        if prev_build:
            self.wv_calib = self.calib_dict[self.arc_master_key]['wavecalib']
            self.wv_maskslits = self.calib_dict[self.arc_master_key]['wvmask']
            self.maskslits += self.wv_maskslits
            return self.wv_calib, self.maskslits

        # No wavelength calibration requested
        if self.par['wavelengths']['reference'] == 'pixel':
            msgs.info("A wavelength calibration will not be performed")
            self.wv_calib = None
            self.wv_maskslits = np.zeros_like(self.maskslits, dtype=bool)
            self.maskslits += self.wv_maskslits
            return self.wv_calib, self.maskslits

        # Grab arc binning (may be different from science!)
        arc_rows = self.fitstbl.find_frames('arc', calib_ID=self.calib_ID, index=True)
        self.arc_files = self.fitstbl.frame_paths(arc_rows)
        binspec, binspat = parse.parse_binning(self.spectrograph.get_meta_value(
            self.arc_files[0], 'binning'))
        # Instantiate
        self.waveCalib = wavecalib.WaveCalib(self.msarc, self.tslits_dict, self.spectrograph, self.par['wavelengths'],
                                             binspectral=binspec, det=self.det,
                                             master_key=self.arc_master_key,
                                             master_dir=self.master_dir,
                                             reuse_masters=self.reuse_masters,
                                             redux_path=self.redux_path, msbpm=self.msbpm)
        # Load from disk (MasterFrame)?
        self.wv_calib, _ = self.waveCalib.master(prev_build=prev_build)
        # Build?
        if self.wv_calib is None:
            self.wv_calib, _ = self.waveCalib.run(skip_QA=(not self.write_qa))
            # Save to Masters
            if self.save_masters:
                self.waveCalib.save_master(self.waveCalib.wv_calib)
        else:
            self.waveCalib.wv_calib = self.wv_calib

        # Create the mask (needs to be done here in case wv_calib was loaded from Masters)
        self.wv_maskslits = self.waveCalib.make_maskslits(self.tslits_dict['slit_left'].shape[1])
        self.maskslits += self.wv_maskslits

        # Save & return
        self.calib_dict[self.arc_master_key]['wavecalib'] = self.wv_calib
        self.calib_dict[self.arc_master_key]['wvmask'] = self.wv_maskslits
        # Return
        return self.wv_calib, self.maskslits

    def get_tilts(self):
        """
        Load or generate the tilts image

        Requirements:
           msarc, tslits_dict, wv_calib, maskslits
           det, par, arc_master_key, spectrograph

        Returns:
            dict, ndarray: :attr:`tilts_dict` dictionary with tilts information (2D)
            and the updated slit mask array

        """
        # Check for existing data
        if not self._chk_objs(['msarc', 'msbpm', 'tslits_dict', 'wv_calib', 'maskslits']):
            msgs.error('dont have all the objects')
            self.tilts_dict = None
            self.wt_maskslits = np.zeros_like(self.maskslits, dtype=bool)
            self.maskslits += self.wt_maskslits
            return self.tilts_dict, self.maskslits

        # Check internals
        self._chk_set(['arc_master_key', 'det', 'calib_ID', 'par'])

        # Return existing data
        prev_build = self.check_for_previous('tilts_dict', self.arc_master_key)
        if prev_build:
            self.tilts_dict = self.calib_dict[self.arc_master_key]['tilts_dict']
            self.wt_maskslits = self.calib_dict[self.arc_master_key]['wtmask']
            self.maskslits += self.wt_maskslits
            return self.tilts_dict, self.maskslits

        # Instantiate
        self.waveTilts = wavetilts.WaveTilts(self.msarc, self.tslits_dict, self.spectrograph,
                                             self.par['tilts'], self.par['wavelengths'], det=self.det,
                                             master_key=self.arc_master_key, master_dir=self.master_dir,
                                             reuse_masters=self.reuse_masters,
                                             redux_path=self.redux_path, bpm=self.msbpm)
        # Master
        self.tilts_dict, _ = self.waveTilts.master(prev_build=prev_build)
        if self.tilts_dict is None:
            # TODO still need to deal with syntax for LRIS ghosts. Maybe we don't need it
            self.tilts_dict, self.wt_maskslits \
                    = self.waveTilts.run(maskslits=self.maskslits,doqa=self.write_qa, show=self.show)
            if self.save_masters:
                self.waveTilts.save_master(self.tilts_dict, steps=self.waveTilts.steps)
        else:
            self.wt_maskslits = np.zeros_like(self.maskslits, dtype=bool)

        # Save & return
        self.calib_dict[self.arc_master_key]['tilts_dict'] = self.tilts_dict
        self.calib_dict[self.arc_master_key]['wtmask'] = self.wt_maskslits
        self.maskslits += self.wt_maskslits
        return self.tilts_dict, self.maskslits

    def run_the_steps(self):
        """
        Run full the full recipe of calibration steps
        """
        for step in self.steps:
            getattr(self, 'get_{:s}'.format(step))()
        msgs.info("Calibration complete!")

    def _chk_set(self, items):
        """
        Check whether a needed attribute has previously been set

        Args:
            items (list): Attributes to check

        """
        for item in items:
            if getattr(self, item) is None:
                msgs.error("Use self.set to specify '{:s}' prior to generating XX".format(item))

    # This is specific to `self.ms*` attributes
    def _chk_objs(self, items):
        """
        Check that the input items exist internally as attributes

        Args:
            items (list):

        Returns:
            bool: True if all exist

        """
        for obj in items:
            if getattr(self, obj) is None:
                msgs.warn("You need to generate {:s} prior to this calibration..".format(obj))
                if obj in ['tslits_dict','maskslits']:
                    msgs.warn("Use get_slits".format(obj))
                else:
                    # Strip ms
                    if obj[0:2] == 'ms':
                        iobj = obj[2:]
                    else:
                        iobj = obj
                    msgs.warn("Use get_{:s}".format(iobj))
                return False
        return True

    def __repr__(self):
        # Generate sets string
        txt = '<{:s}: frame={}, det={}, calib_ID={}'.format(self.__class__.__name__,
                                                          self.frame,
                                                          self.det,
                                                          self.calib_ID)
        txt += '>'
        return txt


class MultiSlitCalibrations(Calibrations):
    """
    Child of Calibrations class for performing multi-slit (and longslit)
    calibrations.
    """
    def __init__(self, fitstbl, par, spectrograph, redux_path=None, reuse_masters=False, save_masters=True,
                 write_qa=True, show = False, steps=None):
        Calibrations.__init__(self, fitstbl, par, spectrograph,
                              redux_path=redux_path, reuse_masters=reuse_masters, save_masters=save_masters,
                              write_qa=write_qa, show = show)
        self.steps = MultiSlitCalibrations.default_steps() if steps is None else steps

    @staticmethod
    def default_steps():
        """
        This defines the steps for calibrations and their order

        Returns:
            list: Calibration steps, in order of execution

        """
        return ['bpm', 'bias', 'arc', 'slits', 'wv_calib', 'tilts',
                'flats', 'wave']


