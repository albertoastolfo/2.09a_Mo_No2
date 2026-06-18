import time
#from DEiger2Client import DEigerClient

#

from EigerClient2022 import EigerClient
# free test!

import subprocess

# DCU network config, please adapt
#DCU_IP = 'applab.dectris.com'
#DCU_PORT = 4011
DCU_IP = '192.168.30.62'
#DCU_IP = '192.168.30.26'
DCU_PORT = 80
# 
newnamepattern='stest'
#filewriter='enabled'
filewriter='disabled'

headerappendix='s2header'
imageappendix='imageappendix'

#detector = DEigerClient(DCU_IP, DCU_PORT)
detector = EigerClient(DCU_IP, DCU_PORT)

# (option) restart API if you need
#print('Restarting...')
#detector.sendSystemCommand('restart')
#print('Sending restart done.')

#time.sleep(3)

# (option) First initialize the detector if you need
#print('Initializing...')
#detector.sendDetectorCommand('initialize')
#print('Initialized')

# windows only: shell=True
proc=subprocess.Popen(['start','python','receiver.py','-i',DCU_IP], shell=True, stdout=subprocess.PIPE)
time.sleep(15)
print("process id= %s", proc.pid)

print('Configure Stream2...')

#detector.setStream2Config('enabled',True)
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

time.sleep(1)

# Enable difference mode, this disables single threshold mode
print('Configure Threshold...')
detector.setDetectorConfig('threshold/2/mode', 'enabled')
#detector.setDetectorConfig('threshold/4/mode', 'enabled')
detector.detectorConfig('threshold/2/mode')
#detector.detectorConfig('threshold/4/mode')
# when enabled, subtracted output is received.
detector.setDetectorConfig('threshold/difference/mode', 'enabled')
# detector.setDetectorConfig('threshold/difference/mode', 'disabled')
detector.setDetectorConfig('threshold/1/energy', 4000)
detector.setDetectorConfig('threshold/2/energy', 30000)

# 2022/12/22 not found below
#detector.setDetectorConfig('threshold/3/energy', 12000)
#detector.setDetectorConfig('threshold/4/energy', 18000)

#ints=triggering,inte=enable
#detector.setDetectorConfig('trigger_mode','ints')

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

#detector.setFileWriterConfig('mode','disabled')

# Set detector configuration, see API reference section 4.1.1
# Only Cu works on the remote test system
# Energy range 6000-17000 on the remote test system
# detector.setDetectorConfig('element', 'Cu')
# detector.setDetectorConfig('photon_energy', 8000.0)
#detector.setDetectorConfig('count_time', 1.0)
print('Arm Setting...')
detector.setDetectorConfig('frame_time', 1)
detector.setDetectorConfig('count_time', 1)
detector.setDetectorConfig('nimages', 10)
detector.setDetectorConfig('ntrigger', 1)
detector.detectorConfig('frame_time')
detector.detectorConfig('nimages')
detector.detectorConfig('ntrigger')

print('Arm Setting done.')
t001=time.perf_counter()
time.sleep(1)
t002=time.perf_counter()
print(f'Confirm time: {t001:0.4f} and {t002:0.4f} for time.sleep(1) ')


# Check threshold settings
print('Photon energy: {} eV'.format(detector.detectorConfig('photon_energy')['value']))
print('Lower threshold energy: {} eV'.format(detector.detectorConfig('threshold/1/energy')['value']))
print('Upper threshold energy: {} eV'.format(detector.detectorConfig('threshold/2/energy')['value']))

print('before taking image ',detector.detectorStatus('state')['value'])

# Make image acquisition
print('Taking image')
t1=time.perf_counter()
detector.sendDetectorCommand('arm')
t2=time.perf_counter()
print('before trigger ',detector.detectorStatus('state')['value'])
t2p2=time.perf_counter()
detector.sendDetectorCommand('trigger')
t3=time.perf_counter()
print('Acquisition finished')
print(f' {t1-t1:0.4f} -- arm -- {t2-t1:0.4f} -- trigger -- {t3-t1:0.4f} ')

print('before disarm ',detector.detectorStatus('state')['value'])

detector.sendDetectorCommand('disarm')

time.sleep(8)

print('after disarm ',detector.detectorStatus('state')['value'])

print('please wait for output of user_data..., then kill output window')


