import time
#from DEiger2Client import DEigerClient

import os
import glob
import shutil
import numpy as np
import subprocess
import matplotlib.pyplot as plt
from tifffile import imread

from EigerClient2022 import EigerClient

import cbor2tiff as c2t # when using snap
#import cbor2tiff as c2t # all other functions



#import shutter_functions as shutter
#import Rigaku_functions as shutter
import Rigaku_shutter_client_functions as shutter

# snap(r'E:\DATA\25_08_14\Alex\snaps');

# EIGER FUNCTIONS based on Melanie Cardona's email and example
# this is for getting dual energy images (while Spiros's example could not do it)
# it needs a receiver function to get the data in real time

# the idea is to save all the data on a temporary folder 'E:\EIGER_DATA' then use the cbor to tif converter to get usable data



def init_receiver():
    
    # start the EIGER2 data receiver pointing on a dummy folder
    
    #windows only: shell=True
    #proc=subprocess.Popen(['start','python','receiver.py','-i','169.254.254.1'], shell=True, stdout=subprocess.PIPE)
    
    proc=subprocess.Popen(['start','python','receiver.py','-d','D:\EIGER_DATA'], shell=True, stdout=subprocess.PIPE)
    
    time.sleep(1)
    print("process id= %s", proc.pid)
    
    return proc

def init():
    
    global detector
    
    # this is to initialize the data receiver and get the detector acquisition to a standard state
    # it is a mix of instructions from Spyros and Melanie
    
    #init_receiver()
    
    #  set all the acquisition without arm and trigger
    
    # RANDOM INITIAL VALUES (can be changed)
    ##################
    exposure_time = 1
    no_frames = 1
    threshold_1 = 5
    threshold_2 = 20
    ##################
    

    # DCU network config
    DCU_IP = '169.254.254.1'
    DCU_PORT = 80
    # 
    newnamepattern='stest'
    #filewriter='enabled'
    filewriter='disabled'
    
    # our dummy name (hard coded, do not change)
    headerappendix=''
    imageappendix='imageappendix'
    
    detector = EigerClient(DCU_IP, DCU_PORT)

    detector.setStreamConfig('mode','enabled')
    detector.setStreamConfig('format','cbor')
    detector.setStreamConfig('header_detail','all')
    detector.setStreamConfig('header_appendix',headerappendix)
    detector.setStreamConfig('image_appendix',imageappendix)
    
    detector.streamConfig('mode')
    testoutput=detector.streamConfig('mode')['value']
    print(f'streanConfig: {testoutput}')
    
    app1=detector.streamConfig('header_appendix')['value']
    app2=detector.streamConfig('image_appendix')['value']
    print(f'header app= {app1} image app= {app2}')
    
    
    print('Configure Stream2 done.')
    
    time.sleep(8)## DO NOT REDUCE FROM 8 - give all 10 of the detector 'workers' time to receive the new basename 'EIGER-TMP'
    
    detector.setDetectorConfig("photon_energy",26000) 
    
    
    # Enable difference mode, this disables single threshold mode
    print('Configure Threshold...')
    
    if threshold_2 != 0:
        detector.setDetectorConfig('threshold/2/mode', 'enabled')
    else:
        detector.setDetectorConfig('threshold/2/mode', 'disabled')
    
    detector.detectorConfig('threshold/2/mode')
    detector.setDetectorConfig('threshold/difference/mode', 'disabled')

    detector.setDetectorConfig('threshold/1/energy', int(threshold_1*1000))
    
    if threshold_2 != 0:
        detector.setDetectorConfig('threshold/2/energy', int(threshold_2*1000))

    print('Configure Threshold done.')
    
    time.sleep(1)
    
    print('Configure monitor...')
    detector.setMonitorConfig('mode','enabled')
    detector.monitorConfig('mode')
    print('Configure monitor done.')
    
    time.sleep(1)
    
    print('Configure Filewriter...')
    detector.setFileWriterConfig('mode',filewriter)
    if filewriter == 'enabled':
        detector.setFileWriterConfig('name_pattern',newnamepattern)
        
    # note: _$id is ignored in basename of stream2 
        detector.fileWriterStatus('buffer_free')
        detector.fileWriterConfig('mode')
        detector.fileWriterConfig('name_pattern')
    
    print('Configure Filewriter done.')
    
    time.sleep(2)
    
    print('Arm Setting...')

    detector.setDetectorConfig('frame_time', exposure_time)
    detector.setDetectorConfig('count_time', exposure_time)
    detector.setDetectorConfig('nimages', no_frames)
    detector.setDetectorConfig('ntrigger', 1)
    detector.setDetectorConfig("virtual_pixel_correction_applied", False)

    
    detector.detectorConfig('frame_time')
    detector.detectorConfig('nimages')
    detector.detectorConfig('ntrigger')
    detector.detectorConfig('virtual_pixel_correction_applied')

    
    # print('Arm Setting done.')
    # t001=time.perf_counter()
    # time.sleep(1)
    # t002=time.perf_counter()
    # print(f'Confirm time: {t001:0.4f} and {t002:0.4f} for time.sleep(1) ')
    
    
    # Check threshold settings
    print('Photon energy: {} eV'.format(detector.detectorConfig('photon_energy')['value']))
    print('Lower threshold energy: {} eV'.format(detector.detectorConfig('threshold/1/energy')['value']))
    print('Upper threshold energy: {} eV'.format(detector.detectorConfig('threshold/2/energy')['value']))
    
    print('before taking image ',detector.detectorStatus('state')['value'])    


# def set_acquisition(exposure_time, no_frames, threshold_1, threshold_2 = 0):

#     # this is an obsolete function    

#     global detector    

#     #  set all the acquisition without triggering it
    

#     ##################
#     # exposure_time     : in [s]
#     # no_frames         : number of frames
#     # threshold_1       : lower threshold in [keV]
#     # threshold_2       : higher threshold in [keV]    
#     # if lower threshold is not set the detector mode will be single threshold
#     ##################
    
#     # clear the temporary folder
#     directory=r'E:\EIGER_DATA'
#     os.chdir(directory)
#     files=glob.glob('*.cbor')
#     for filename in files:
#         os.unlink(filename)

#     # NB: when a single scan runs it created a '_tiff' folder. Here I cancel it
#     try:
#         shutil.rmtree('E:\_tiff')
#     except:
#         pass


#     # DCU network config
#     DCU_IP = '169.254.254.1'
#     DCU_PORT = 80
#     # 
#     newnamepattern='stest'
#     #filewriter='enabled'
#     filewriter='disabled'
    
#     headerappendix='EIGER-TMP'
#     imageappendix='imageappendix'
    
#     detector = EigerClient(DCU_IP, DCU_PORT)
    

#     detector.setStreamConfig('mode','enabled')
#     detector.setStreamConfig('format','cbor')
#     detector.setStreamConfig('header_detail','all')
#     detector.setStreamConfig('header_appendix',headerappendix)
#     detector.setStreamConfig('image_appendix',imageappendix)
    
#     detector.streamConfig('mode')
#     testoutput=detector.streamConfig('mode')['value']
#     print(f'streanConfig: {testoutput}')
    
#     app1=detector.streamConfig('header_appendix')['value']
#     app2=detector.streamConfig('image_appendix')['value']
#     print(f'header app= {app1} image app= {app2}')
    
    
#     print('Configure Stream2 done.')
    
#     time.sleep(1)
    
#     # Enable difference mode, this disables single threshold mode
#     print('Configure Threshold...')
    
#     # here I decide if to use one of two thresholds
    
#     if threshold_2 != 0:
#         detector.setDetectorConfig('threshold/2/mode', 'enabled')
#     else:
#         detector.setDetectorConfig('threshold/2/mode', 'disabled')
    
    
#     detector.detectorConfig('threshold/2/mode')
#     detector.setDetectorConfig('threshold/difference/mode', 'disabled')

#     detector.setDetectorConfig('threshold/1/energy', int(threshold_1*1000))
    
#     if threshold_2 != 0:
#         detector.setDetectorConfig('threshold/2/energy', int(threshold_2*1000))

#     print('Configure Threshold done.')
    
#     time.sleep(1)
    
#     print('Configure monitor...')
#     detector.setMonitorConfig('mode','enabled')
#     detector.monitorConfig('mode')
#     print('Configure monitor done.')
    
#     time.sleep(1)
    
#     print('Configure Filewriter...')
#     detector.setFileWriterConfig('mode',filewriter)
#     if filewriter == 'enabled':
#         detector.setFileWriterConfig('name_pattern',newnamepattern)
        
#     # note: _$id is ignored in basename of stream2 
#         detector.fileWriterStatus('buffer_free')
#         detector.fileWriterConfig('mode')
#         detector.fileWriterConfig('name_pattern')
    
#     print('Configure Filewriter done.')
    
#     time.sleep(2)
    
#     print('Arm Setting...')

#     detector.setDetectorConfig('frame_time', exposure_time)
#     detector.setDetectorConfig('count_time', exposure_time)
#     detector.setDetectorConfig('nimages', no_frames)
#     detector.setDetectorConfig('ntrigger', 1)    
    
#     detector.detectorConfig('frame_time')
#     detector.detectorConfig('nimages')
#     detector.detectorConfig('ntrigger')
    
#     print('Arm Setting done.')
#     t001=time.perf_counter()
#     time.sleep(1)
#     t002=time.perf_counter()
#     print(f'Confirm time: {t001:0.4f} and {t002:0.4f} for time.sleep(1) ')
    
    
#     # Check threshold settings
#     print('Photon energy: {} eV'.format(detector.detectorConfig('photon_energy')['value']))
#     print('Lower threshold energy: {} eV'.format(detector.detectorConfig('threshold/1/energy')['value']))
#     print('Upper threshold energy: {} eV'.format(detector.detectorConfig('threshold/2/energy')['value']))
    
#     print('before taking image ',detector.detectorStatus('state')['value'])
    
#     # Make image acquisition
#     print('Taking image')
#     t1=time.perf_counter()
#     detector.sendDetectorCommand('arm')
#     t2=time.perf_counter()
#     print('before trigger ',detector.detectorStatus('state')['value'])
    
#     print('Done! Waiting for the trigger')
    
#     return detector

def arm():
    
    # arms the detector with the exposure time and setting as it is (no changes done here)
    # after this you can start the acquisition with a 'trigger()' command
    
    # TEMPORARY FOLDER
    # clear the temporary folder
    directory=r'D:\EIGER_DATA'
    os.chdir(directory)
    files=glob.glob('*.cbor')
    for filename in files:
        os.unlink(filename)

    # NB: when a single scan runs it created a '_tiff' folder. Here I cancel it
    try:
        shutil.rmtree('D:\_tiff')
    except:
        pass
    
    
    detector.sendDetectorCommand('arm')
    
    time.sleep(2)

def disarm():

    detector.sendDetectorCommand('disarm')
    time.sleep(1)
    print('after disarm ', detector.detectorStatus('state')['value'])

    
def arm_keepImages():
    # not Alberto's version: don't you use it!
    # arms the detector with the exposure time and setting as it is (no changes done here)
    # after this you can start the acquisition with a 'trigger()' command
    
    # TEMPORARY FOLDER
    # clear the temporary folder
    directory=r'D:\EIGER_DATA'
    os.chdir(directory)
    # files=glob.glob('*.cbor')
    # for filename in files:
    #     os.unlink(filename)

    # NB: when a single scan runs it created a '_tiff' folder. Here I cancel it
    # try:
    #     shutil.rmtree('E:\_tiff')
    # except:
    #     pass
    
    
    detector.sendDetectorCommand('arm')
    
    time.sleep(2)    

def trigger(disarm=1):# disarm by default to work with initial versions of code written by Alberto and Ian - set to zero if sending multiple triggers
    
    # send the trigger after you have armed the detector
    
    t1=time.perf_counter()
    print('send Trigger -')
    detector.sendDetectorCommand('trigger')
    t2=time.perf_counter()
    print('Acquisition finished')
    print(f' -- trigger -- {t2-t1:0.4f} ')
    
    # print('before disarm ',detector.detectorStatus('state')['value'])
    
    if(disarm):
        detector.sendDetectorCommand('disarm')
        time.sleep(1)
        print('after disarm ',detector.detectorStatus('state')['value'])
    else:
        print('Detector still armed; status ',detector.detectorStatus('state')['value'])
    
    #print('please wait for output of user_data..., then kill output window')

def snap(output_path, name=None):
    
    # just a quick way to take and image with the settings as they are
    
    #shutter.shutter('open')
    shutter.Open_Shutter()

    arm()
    
    trigger()
    
    #shutter.shutter('close')
    shutter.Close_Shutter()    

    
    ths = get_thresholds()
    base_name = 'Image_Th1_'+str(ths[0]).replace('.', 'p') + '_Th2_' + str(ths[1]).replace('.', 'p')
    
    if name is not None:
        base_name += f"_{name}"
    
    
    num = len(glob.glob(os.path.join(output_path, "*.tif"))) + 1
    im_name = f"{base_name}_{num:03d}"
    
    # c2t.subset_mydecoder_tif(r'D:\EIGER_DATA', output_path,im_name)
    # c2t.decoder_tif(r'D:\EIGER_DATA', output_path)
    c2t.decoder_tif_khush(r'D:\EIGER_DATA', output_path, im_name)    
    
    
    file_type = r"\\*tif"  # Replace 'type' with the desired file extension (e.g., '.csv', '.txt')
    files = glob.glob(output_path + file_type)
    sorted_files = sorted(files, key=os.path.getctime, reverse=True)
    
    # try:
    #     im_th2 = sorted_files[0]
    #     im_th2 = imread(im_th2)
    #     ul2 = np.percentile(im_th2[0,:,:],90)
    #     plt.subplot(2,1,2)
    #     plt.imshow(im_th2[0,:,:],vmin=0,vmax=ul2)
    #     plt.colorbar()
    #     plt.title('Th2')
    #     plt.show()
        
    #     im_th1 = sorted_files[1]
    #     im_th1 = imread(im_th1)
    #     ul1 = np.percentile(im_th1[0,:,:],90)
        
    #     plt.subplot(2,1,1)
    #     plt.imshow(im_th1[0,:,:],vmin=0,vmax=ul1)
    #     plt.colorbar()
    #     plt.title('Th1')
        
    # except:
    #     im_th2 = sorted_files[0]
    #     im_th2 = imread(im_th2)
    #     ul2 = np.percentile(im_th2[:, :], 90)
    #     plt.subplot(2, 1, 2)
    #     plt.imshow(im_th2[:, :], vmin=0, vmax=ul2)
    #     plt.colorbar()
    #     plt.title('Th2')
    #     plt.show()

            
    
    
    
def AcquireWaitSave(image_name):
    
    # image_name with full address and name
    
    # I take the path and image name from the entry
    folders = image_name.split('\\')
    
    path = ''
    
    for i in folders[0:-1]:
        path = path + i + '/'
    path = path[0:-1]
    
    
    name = image_name.split('\\')[-1]
    
    print(path)
    print(name)
    
    # acquire image 
    
    arm()
    
    trigger()
    
    roi_y = np.array([0,256])
    roi_x = np.array([465,850])
    #c2t.mydecoder_tif(r'D:\EIGER_DATA', path, name,1)
    c2t.subset_mydecoder_tif(r'D:\EIGER_DATA', path,roi_y,roi_x, name,1)
    print('Image saved')
    

def get_thresholds():

    # get the set thresholds
    
    thresholds = np.zeros(2)
    
    for i in [1, 2]:
        param = f'threshold/{i}'
        
        thresholds[i-1] =  detector.detectorConfig(f'{param}/energy')['value'] /1000
        
        print(param, detector.detectorConfig(f'{param}/mode')['value'], thresholds[i-1], '[keV]')

       

    # Check threshold settings
    print('Photon energy: {} eV'.format(detector.detectorConfig('photon_energy')['value']))
    print('Lower threshold energy: {} eV'.format(detector.detectorConfig('threshold/1/energy')['value']))
    print('Upper threshold energy: {} eV'.format(detector.detectorConfig('threshold/2/energy')['value']))

    return thresholds 

def set_thresholds(threshold_1, threshold_2 = 0):

    # set the thresholds in [keV]    

    # here I decide if to use one of two thresholds
    
    if threshold_2 != 0:
        detector.setDetectorConfig('threshold/2/mode', 'enabled')
    else:
        detector.setDetectorConfig('threshold/2/mode', 'disabled')
    
    detector.detectorConfig('threshold/2/mode')

    detector.setDetectorConfig('threshold/difference/mode', 'disabled')

    if threshold_2 != 0:
        detector.setDetectorConfig('threshold/1/energy', int(threshold_1*1000))
        detector.setDetectorConfig('threshold/2/energy', int(threshold_2*1000))
    else:
        detector.setDetectorConfig('threshold/1/energy', int(threshold_1*1000))


def set_exposure_time(exposure_time):
    
    # set the exposure time
    
    detector.setDetectorConfig("count_time", exposure_time)
    detector.setDetectorConfig('frame_time', exposure_time)

def set_nimages(n_images):
    
    detector.setDetectorConfig("nimages",int(round(n_images)))
    detector.setDetectorConfig('ntrigger', 1)    
    
def set_nimages_ntriggers(n_images,n_triggers):
    
    detector.setDetectorConfig("nimages",int(round(n_images)))
    detector.setDetectorConfig('ntrigger', int(round(n_triggers)))        

def HV_reset():
    
    detector.sendDetectorCommand("hv_reset")
    # default reset time is 30s
    time.sleep(30)


# def snap(exposure_time, no_frames, threshold_1, threshold_2 = 0):

#     ##################
#     # exposure_time     : in [s]
#     # no_frames         : number of frames
#     # threshold_1       : lower threshold in [keV]
#     # threshold_2       : higher threshold in [keV]    
#     # if lower threshold is not set the detector mode will be single threshold
#     ##################
    


#     # DCU network config, please adapt
#     #DCU_IP = 'applab.dectris.com'
#     #DCU_PORT = 4011
#     DCU_IP = '169.254.254.1'
#     #DCU_IP = '192.168.30.26'
#     DCU_PORT = 80
#     # 
#     newnamepattern='stest'
#     #filewriter='enabled'
#     filewriter='disabled'
    
#     headerappendix='s2header'
#     imageappendix='imageappendix'
    
#     #detector = DEigerClient(DCU_IP, DCU_PORT)
#     detector = EigerClient(DCU_IP, DCU_PORT)
    
#     # (option) restart API if you need
#     #print('Restarting...')
#     #detector.sendSystemCommand('restart')
#     #print('Sending restart done.')
    
#     #time.sleep(3)
    
#     # (option) First initialize the detector if you need
#     #print('Initializing...')
#     #detector.sendDetectorCommand('initialize')
#     #print('Initialized')
    
#     # windows only: shell=True
#     # proc=subprocess.Popen(['start','python','receiver.py','-i',DCU_IP], shell=True, stdout=subprocess.PIPE)
#     # time.sleep(15)
#     # print("process id= %s", proc.pid)
    
#     # print('Configure Stream2...')
    
#     #detector.setStream2Config('enabled',True)
#     detector.setStreamConfig('mode','enabled')
#     detector.setStreamConfig('format','cbor')
#     detector.setStreamConfig('header_detail','all')
#     detector.setStreamConfig('header_appendix',headerappendix)
#     detector.setStreamConfig('image_appendix',imageappendix)
    
#     detector.streamConfig('mode')
#     testoutput=detector.streamConfig('mode')['value']
#     print(f'streanConfig: {testoutput}')
    
#     app1=detector.streamConfig('header_appendix')['value']
#     app2=detector.streamConfig('image_appendix')['value']
#     print(f'header app= {app1} image app= {app2}')
    
    
#     print('Configure Stream2 done.')
    
#     time.sleep(1)
    
#     # Enable difference mode, this disables single threshold mode
#     print('Configure Threshold...')
    
#     # here I decide if to use one of two thresholds
    
#     if threshold_2 != 0:
#         detector.setDetectorConfig('threshold/2/mode', 'enabled')
#     else:
#         detector.setDetectorConfig('threshold/2/mode', 'disabled')
    
    
#     #detector.setDetectorConfig('threshold/4/mode', 'enabled')
#     detector.detectorConfig('threshold/2/mode')
#     #detector.detectorConfig('threshold/4/mode')
#     # when enabled, subtracted output is received.
#     #detector.setDetectorConfig('threshold/difference/mode', 'enabled')
#     detector.setDetectorConfig('threshold/difference/mode', 'disabled')
#     # detector.setDetectorConfig('threshold/1/energy', 4000)
#     # detector.setDetectorConfig('threshold/2/energy', 30000)

#     detector.setDetectorConfig('threshold/1/energy', int(threshold_1*1000))
#     detector.setDetectorConfig('threshold/2/energy', int(threshold_2*1000))

    
#     # 2022/12/22 not found below
#     #detector.setDetectorConfig('threshold/3/energy', 12000)
#     #detector.setDetectorConfig('threshold/4/energy', 18000)
    
#     #ints=triggering,inte=enable
#     #detector.setDetectorConfig('trigger_mode','ints')
    
#     print('Configure Threshold done.')
    
#     time.sleep(1)
    
#     print('Configure monitor...')
#     detector.setMonitorConfig('mode','enabled')
#     detector.monitorConfig('mode')
#     print('Configure monitor done.')
    
#     time.sleep(1)
    
#     print('Configure Filewriter...')
#     detector.setFileWriterConfig('mode',filewriter)
#     if filewriter == 'enabled':
#         detector.setFileWriterConfig('name_pattern',newnamepattern)
        
#     # note: _$id is ignored in basename of stream2 
#         detector.fileWriterStatus('buffer_free')
#         detector.fileWriterConfig('mode')
#         detector.fileWriterConfig('name_pattern')
    
#     print('Configure Filewriter done.')
    
#     time.sleep(2)
    
#     #detector.setFileWriterConfig('mode','disabled')
    
#     # Set detector configuration, see API reference section 4.1.1
#     # Only Cu works on the remote test system
#     # Energy range 6000-17000 on the remote test system
#     # detector.setDetectorConfig('element', 'Cu')
#     # detector.setDetectorConfig('photon_energy', 8000.0)
#     #detector.setDetectorConfig('count_time', 1.0)
#     print('Arm Setting...')
#     # detector.setDetectorConfig('frame_time', 1)
#     # detector.setDetectorConfig('count_time', 1)
#     # detector.setDetectorConfig('nimages', 10)
#     # detector.setDetectorConfig('ntrigger', 1)
    
#     detector.setDetectorConfig('frame_time', exposure_time)
#     detector.setDetectorConfig('count_time', exposure_time)
#     detector.setDetectorConfig('nimages', no_frames)
#     detector.setDetectorConfig('ntrigger', 1)    
    
    
    
#     detector.detectorConfig('frame_time')
#     detector.detectorConfig('nimages')
#     detector.detectorConfig('ntrigger')
    
#     print('Arm Setting done.')
#     t001=time.perf_counter()
#     time.sleep(1)
#     t002=time.perf_counter()
#     print(f'Confirm time: {t001:0.4f} and {t002:0.4f} for time.sleep(1) ')
    
    
#     # Check threshold settings
#     print('Photon energy: {} eV'.format(detector.detectorConfig('photon_energy')['value']))
#     print('Lower threshold energy: {} eV'.format(detector.detectorConfig('threshold/1/energy')['value']))
#     print('Upper threshold energy: {} eV'.format(detector.detectorConfig('threshold/2/energy')['value']))
    
#     print('before taking image ',detector.detectorStatus('state')['value'])
    
#     # Make image acquisition
#     print('Taking image')
#     t1=time.perf_counter()
#     detector.sendDetectorCommand('arm')
#     t2=time.perf_counter()
#     print('before trigger ',detector.detectorStatus('state')['value'])
#     t2p2=time.perf_counter()
#     detector.sendDetectorCommand('trigger')
#     t3=time.perf_counter()
#     print('Acquisition finished')
#     print(f' {t1-t1:0.4f} -- arm -- {t2-t1:0.4f} -- trigger -- {t3-t1:0.4f} ')
    
#     print('before disarm ',detector.detectorStatus('state')['value'])
    
#     detector.sendDetectorCommand('disarm')
    
#     time.sleep(8)
    
#     print('after disarm ',detector.detectorStatus('state')['value'])
    
#     print('please wait for output of user_data..., then kill output window')


    

