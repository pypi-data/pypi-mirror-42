# Odds and ends in support of tests
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import pytest
import numpy as np
import copy

from astropy import time

from pypeit import arcimage
from pypeit import traceslits
from pypeit import wavecalib
from pypeit import wavetilts
from pypeit.spectrographs.util import load_spectrograph
from pypeit.metadata import PypeItMetaData

# Create a decorator for tests that require the PypeIt dev suite
dev_suite_required = pytest.mark.skipif(os.getenv('PYPEIT_DEV') is None,
                                        reason='test requires dev suite')

def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)

def dummy_fitstbl(nfile=10, spectro_name='shane_kast_blue', directory='', notype=False):
    """
    Generate a dummy fitstbl for testing

    Parameters
    ----------
    nfile : int, optional
      Number of files to mimic
    spectro_name : str, optional
      Name of spectrograph to mimic
    notype : bool (optional)
      If True, do not add image type info to the fitstbl

    Returns
    -------
    fitstbl : PypeItMetaData

    """
    fitsdict = {}
    fitsdict['index'] = np.arange(nfile)
    fitsdict['directory'] = [directory]*nfile
    fitsdict['filename'] = ['b{:03d}.fits.gz'.format(i) for i in range(nfile)]
    # TODO: The below will fail at 60
    dates = ['2015-01-23T00:{:02d}:11.04'.format(i) for i in range(nfile)]
    ttime = time.Time(dates, format='isot')
    fitsdict['mjd'] = ttime.mjd
    fitsdict['target'] = ['Dummy']*nfile
    fitsdict['ra'] = ['00:00:00']*nfile
    fitsdict['dec'] = ['+00:00:00']*nfile
    fitsdict['exptime'] = [300.] * nfile
    fitsdict['dispname'] = ['600/4310'] * nfile
    fitsdict['dichroic'] = ['560'] * nfile
    fitsdict["binning"] = ['1,1']*nfile
    fitsdict["airmass"] = [1.0]*nfile

    if spectro_name == 'shane_kast_blue':
        fitsdict['numamplifiers'] = [1] * nfile
        # Lamps
        for i in range(1,17):
            fitsdict['lampstat{:02d}'.format(i)] = ['off'] * nfile
        fitsdict['exptime'][0] = 0        # Bias
        fitsdict['lampstat06'][1] = 'on'  # Arc
        fitsdict['exptime'][1] = 30       # Arc
        fitsdict['lampstat01'][2] = 'on'  # Trace, pixel, slit flat
        fitsdict['lampstat01'][3] = 'on'  # Trace, pixel, slit flat
        fitsdict['exptime'][2] = 30     # flat
        fitsdict['exptime'][3] = 30     # flat
        fitsdict['ra'][4] = '05:06:36.6'  # Standard
        fitsdict['dec'][4] = '52:52:01.0'
        fitsdict['airmass'][4] = 1.2
        fitsdict['ra'][5] = '07:06:23.45' # Random object
        fitsdict['dec'][5] = '+30:20:50.5'
        fitsdict['decker'] = ['0.5 arcsec'] * nfile

    # arrays
    for k in fitsdict.keys():
        fitsdict[k] = np.array(fitsdict[k])

    spectrograph = load_spectrograph(spectro_name)
    fitstbl = PypeItMetaData(spectrograph, spectrograph.default_pypeit_par(), data=fitsdict)
    fitstbl['instrume'] = spectro_name
    type_bits = np.zeros(len(fitstbl), dtype=fitstbl.type_bitmask.minimum_dtype())

    # Image typing
    if not notype:
        if spectro_name == 'shane_kast_blue':
            #fitstbl['sci_ID'] = 1  # This links all the files to the science object
            type_bits[0] = fitstbl.type_bitmask.turn_on(type_bits[0], flag='bias')
            type_bits[1] = fitstbl.type_bitmask.turn_on(type_bits[1], flag='arc')
            type_bits[2:4] = fitstbl.type_bitmask.turn_on(type_bits[2:4], flag=['pixelflat', 'trace'])
            type_bits[4] = fitstbl.type_bitmask.turn_on(type_bits[4], flag='standard')
            type_bits[5:] = fitstbl.type_bitmask.turn_on(type_bits[5:], flag='science')
            fitstbl.set_frame_types(type_bits)
            # Calibration groups
            cfgs = fitstbl.unique_configurations(ignore_frames=['bias', 'dark'])
            fitstbl.set_configurations(cfgs)
            fitstbl.set_calibration_groups(global_frames=['bias', 'dark'])

    return fitstbl


def load_kast_blue_masters(get_spectrograph=False, aimg=False, tslits=False, tilts=False,
                           datasec=False, wvcalib=False):
    """
    Load up the set of shane_kast_blue master frames

    Args:
        get_spectrograph:
        aimg:
        tslits:
        tilts:
        datasec:
        wvcalib:

    Returns:

    """

    spectrograph = load_spectrograph('shane_kast_blue')
    spectrograph.naxis = (2112,350)     # Image shape with overscan

    root_path = data_path('MF') if os.getenv('PYPEIT_DEV') is None \
                    else os.path.join(os.getenv('PYPEIT_DEV'), 'Cooked', 'MF')
    master_dir = root_path+'_'+spectrograph.spectrograph

    reuse_masters = True

    # Load up the Masters
    ret = []

    if get_spectrograph:
        ret.append(spectrograph)

    master_key = 'A_1_01'
    if aimg:
        AImg = arcimage.ArcImage(spectrograph, master_key=master_key, master_dir=master_dir, reuse_masters=reuse_masters)
        msarc, _ = AImg.load_master(AImg.ms_name)
        ret.append(msarc)

    if tslits:
        traceSlits = traceslits.TraceSlits(None,spectrograph,None)
        # TODO: Should this be json now?
        tslits_dict, mstrace = traceSlits.load_master(os.path.join(master_dir,'MasterTrace_A_1_01.fits'))
        # This is a bit of a hack, but I'm adding the mstrace to the dict since we need it in the flat field test
        tslits_dict['mstrace'] = mstrace
        ret.append(tslits_dict)

    if tilts:
        wvTilts = wavetilts.WaveTilts(None, None, spectrograph, None, None, master_key=master_key,
                                      master_dir=master_dir, reuse_masters=reuse_masters)
        tilts_dict, _ = wvTilts.master()
        ret.append(tilts_dict)

    if datasec:
        datasec_img = spectrograph.get_datasec_img(data_path('b1.fits.gz'), 1)
        ret.append(datasec_img)

    if wvcalib:
        Wavecalib = wavecalib.WaveCalib(None, None, spectrograph,
                                        spectrograph.default_pypeit_par()['calibrations']['wavelengths'],
                                        master_key=master_key,
                                        master_dir=master_dir, reuse_masters=reuse_masters)
        wv_calib, _ = Wavecalib.master()
        ret.append(wv_calib)


    # Return
    return ret

def instant_traceslits(mstrace_file, det=None):
    """
    Instantiate a TraceSlits object from the master file

    The loaded tslits_dict is set as the atribute

    Args:
        mstrace_file (str):
        det (int, optional):

    Returns:
        Spectrograph, TraceSlits:

    """
    # Load
    tslits_dict, mstrace = traceslits.load_tslits(mstrace_file)
    # Instantiate
    spectrograph = load_spectrograph(tslits_dict['spectrograph'])
    par = spectrograph.default_pypeit_par()
    msbpm = spectrograph.bpm(shape=mstrace.shape, det=det)
    binning = tslits_dict['binspectral'], tslits_dict['binspatial']
    traceSlits = traceslits.TraceSlits(mstrace, spectrograph, par['calibrations']['slits'],
                                       msbpm=msbpm, binning=binning)
    traceSlits.tslits_dict = copy.deepcopy(tslits_dict)
    return spectrograph, traceSlits
