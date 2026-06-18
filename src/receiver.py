import zmq
import logging, os, argparse
import multiprocessing
import time

logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)

from EigerClient2022 import EigerClient

import decoding
import NameSubscriber

portNamePattern = "6666"
addressNamePattern = f'tcp://127.0.0.1:{portNamePattern}'
topic = 9999

#--- user must specify the following!
#ipadd1='192.168.20.170'
ipadd1='169.254.254.1'
port1=31001
#or, default 31001, other case=6025
outdir1='testdir'
verbosity=10
converttif=False
# is 100, change 10
#---

def receiver(id, ip, port, outDir, baseName='', dumptif=converttif):
    
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect(f'tcp://{ip}:{port}')
    logging.info(f'receiver {id} connected to tcp://{ip}:{port}, printing after {verbosity} received frames')
    
    namePoller = NameSubscriber.NameSubscriber(id)
    
    msgs = 0
    while True:
        try:
            newName = namePoller.poll()
            if newName is not None:
                baseName = newName
                logging.info(f'worker {id} got new basename {baseName}')
            
            if receiver.poll(10):
                frames = receiver.recv(copy = False)
                msgs += 1
                if msgs%verbosity == 0:
                    logging.info(f'worker {id} received {msgs} frames')
                decoding.processMessage(frames, outDir, baseName, dumptif)
        
        except Exception as e:
            logging.error(e)

            
def statusPoller(ip):
#    c = EigerClient.EigerClient(ip)
    c = EigerClient(ip)
    
    logging.info(f'enabling stream2 and setting header details to all')
#    c.setStream2Config('enabled', True)
#    c.setStream2Config('start_fields', 'all')
    c.setStreamConfig('mode', 'enabled')
    c.setStreamConfig('format', 'cbor')
    c.setStreamConfig('header_detail', 'all')
    
    
    while True:
        try:
#            enabled = c.stream2Config('enabled')['value']
            enabled = c.streamConfig('mode')['value']
            status = c.detectorStatus('state')['value']
            temp = c.detectorStatus('temperature')['value']
            hv = c.detectorStatus('high_voltage/state')['value']
            
            logging.info(f'status: detector {status}\t temp: {temp:.2f} C\t HV: {hv}\t stream2 mode: {enabled}')
            
        except Exception as e:
            logging.error(e)
        
        finally:
            time.sleep(2)
       

# new from 2022.1

def enableStream2(ip):
    
    c = EigerClient(ip)
#    c = EigerClient.EigerClient(ip)
    
    logging.info(f'enabling stream2 and setting header details to all')
#    c.setStream2Config('enabled', True)
#    c.setStream2Config('start_fields', 'all')
    c.setStreamConfig('mode','enabled')
    c.setStreamConfig('format', 'cbor')
    c.setStreamConfig('header_detail', 'all')


def getNamePattern(detIP):
    try:
#        c = EigerClient.EigerClient(detIP)
        c = EigerClient(detIP)
        
#        namePattern = c.fileWriterConfig('name_pattern')['value']
        namePattern = c.streamConfig('header_appendix')['value']

        return namePattern.replace('_$id', '')
    
    except Exception as e:
        logging.error(e)
        return None


def publishNamePattern(detIP):

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(addressNamePattern)
    logging.info(f'publishing NamePattern on {addressNamePattern}')
    
    fname = ""

    while True:
        namePattern = getNamePattern(detIP)
        if fname != namePattern:
            fname = namePattern
            logging.info(f'name pattern changed to {fname}')
            message = f'{topic} {fname}'
            socket.send_string(message)
        time.sleep(1)


def parseArgs():
    parser = argparse.ArgumentParser(description = "receive and dump zmq messages to file")

#    parser.add_argument("-i", "--ip", help="EIGER2 host ip", type=str, required=True)
    parser.add_argument("-i", "--ip", help="EIGER2 host ip", type=str, default=ipadd1)
#    parser.add_argument("-p", "--port", help="EIGER2 stream2 port", type=int, default=31001)
    parser.add_argument("-p", "--port", help="EIGER2 stream2 port", type=int, default=port1)  
    parser.add_argument("-n", "--nProcesses", help="number of receiver processes", type=int, default=10)
# was 4, change 10
#    parser.add_argument("-d", "--dir", help="/path/to/output/dir", default = ".")
    parser.add_argument("-d", "--dir", help="/path/to/output/dir", default = outdir1)
    parser.add_argument("-f", "--fname", help="basename for file", default = "")
    parser.add_argument("-dumptif", "--dumptif", help="dump tif from image cbor", type=bool, default=False)

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parseArgs()
    
    os.makedirs(args.dir, exist_ok=True)
    
    multiprocessing.Process(target=statusPoller, args=(args.ip, )).start()
    
    enableStream2(args.ip)

    multiprocessing.Process(target=publishNamePattern, args=(args.ip, )).start()
   
    for id in range(args.nProcesses):
        multiprocessing.Process(target=receiver, args=(id, args.ip, args.port, args.dir, args.fname, args.dumptif)).start()
