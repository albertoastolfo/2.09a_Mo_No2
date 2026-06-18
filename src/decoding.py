import cbor2
from dectris.compression import decompress
import numpy as np
import logging, os
import tifffile,glob
import time

#
# tested with 2022.1.1
# install dependencies:
# pip install cbor2 dectris-compression~=0.2.1 numpy zmq
# pip install git+https://github.com/dectris/compression~=0.2.1
#

logging.basicConfig()
log = logging.getLogger(__name__)

def decode_multi_dim_array(tag, column_major):
    dimensions, contents = tag.value
    if isinstance(contents, list):
        array = np.empty((len(contents),), dtype=object)
        array[:] = contents
    elif isinstance(contents, (np.ndarray, np.generic)):
        array = contents
    else:
        raise cbor2.CBORDecodeValueError("expected array or typed array")
    return array.reshape(dimensions, order="F" if column_major else "C")


def decode_typed_array(tag, dtype):
    if not isinstance(tag.value, bytes):
        raise cbor2.CBORDecodeValueError("expected byte string in typed array")
    return np.frombuffer(tag.value, dtype=dtype)

def decode_dectris_compression(tag):
    algorithm, elem_size, encoded = tag.value
    return decompress(encoded, algorithm, elem_size=elem_size)

tag_decoders = {
    40: lambda tag: decode_multi_dim_array(tag, column_major=False),
    64: lambda tag: decode_typed_array(tag, dtype="u1"),
    65: lambda tag: decode_typed_array(tag, dtype=">u2"),
    66: lambda tag: decode_typed_array(tag, dtype=">u4"),
    67: lambda tag: decode_typed_array(tag, dtype=">u8"),
    68: lambda tag: decode_typed_array(tag, dtype="u1"),
    69: lambda tag: decode_typed_array(tag, dtype="<u2"),
    70: lambda tag: decode_typed_array(tag, dtype="<u4"),
    71: lambda tag: decode_typed_array(tag, dtype="<u8"),
    72: lambda tag: decode_typed_array(tag, dtype="i1"),
    73: lambda tag: decode_typed_array(tag, dtype=">i2"),
    74: lambda tag: decode_typed_array(tag, dtype=">i4"),
    75: lambda tag: decode_typed_array(tag, dtype=">i8"),
    77: lambda tag: decode_typed_array(tag, dtype="<i2"),
    78: lambda tag: decode_typed_array(tag, dtype="<i4"),
    79: lambda tag: decode_typed_array(tag, dtype="<i8"),
    80: lambda tag: decode_typed_array(tag, dtype=">f2"),
    81: lambda tag: decode_typed_array(tag, dtype=">f4"),
    82: lambda tag: decode_typed_array(tag, dtype=">f8"),
    83: lambda tag: decode_typed_array(tag, dtype=">f16"),
    84: lambda tag: decode_typed_array(tag, dtype="<f2"),
    85: lambda tag: decode_typed_array(tag, dtype="<f4"),
    86: lambda tag: decode_typed_array(tag, dtype="<f8"),
    87: lambda tag: decode_typed_array(tag, dtype="<f16"),
    1040: lambda tag: decode_multi_dim_array(tag, column_major=True),
    56500: lambda tag: decode_dectris_compression(tag),  
}


def tag_hook(decoder, tag):
    tag_decoder = tag_decoders.get(tag.tag)
    return tag_decoder(tag) if tag_decoder else tag


def decompress_channel_data(channel):
    data = channel["data"]

    if isinstance(data, (np.ndarray, np.generic)):
        return data

    dimensions, encoded = data

    compression = channel["compression"]
    data_type = channel["data_type"]
    dtype = {"uint8": "u1", "uint16le": "<u2", "uint32le": "<u4"}[data_type]
#    elem_size = {"uint8": 1, "uint16le": 2, "uint32le": 4}[data_type]

#    if compression == "bslz4":
#        decompressed = decompress(encoded, "bslz4-h5", elem_size=elem_size)
    if compression == "lz4":
        decompressed = decompress(encoded, "lz4-h5")
    elif compression == "none":
        decompressed = encoded
    else:
        raise NotImplementedError(f"unknown compression: {compression}")

    return np.frombuffer(decompressed, dtype=dtype).reshape(dimensions)


def processMessage(frame, outDir, basename=None, dumptif=False):
    message = cbor2.loads(frame, tag_hook=tag_hook)
    if basename is None:
        basename = message["series_unique_id"]
    
    
    if message["type"] == "start":
# series_number->series_id        
        log.info(f'**** start series {message["series_id"]}')
        ts=time.perf_counter()
        print('at start= ', ts)
        for key, value in message.items():
            print(key, value)    
            
        fname = f'{basename}_s{message["series_id"]:06d}_metaData.cbor'
        path = os.path.join(outDir, fname)
        with open(path, 'wb') as f:
            f.write(frame)   
                
    
    elif message["type"] == "end":
# series_number->series_id        
        log.info(f'**** end series {message["series_id"]}')
        te1=time.perf_counter()
        print('end 1= ',te1)
        
# if you want to convert tiff immidiately...       
        outDirTiff = os.path.dirname(outDir) + '_tiff'
        os.makedirs(outDirTiff, exist_ok=True)
#series_number->series_id, image_number->image_id        
        files=glob.glob(os.path.join(outDir,f'{basename}_{message["series_id"]:06d}_*.cbor'))
        for fname in files:
            with open(fname, 'rb') as f:
                message2 = cbor2.loads(f.read(), tag_hook=tag_hook)
            if dumptif == True:
                fnameout = f'{basename}_{message["series_id"]:06d}_{message2["image_id"]:06d}.tif'
                path = os.path.join(outDirTiff, fnameout)
                for threshold, data in message2["data"].items():
                    imgName = path.replace('.tif', f'_{threshold}.tif')
                    tifffile.imsave(imgName, data)    
                    
#                for channel in message2["channels"]:
#                    channel["data"] = decompress_channel_data(channel)  
#                    thresholds = "_".join(map(str, channel["thresholds"]))  
#                    imgName = path.replace('.tif', f'_{thresholds}.tif')
#                    tifffile.imsave(imgName, channel["data"])       

# it add measurement time???
            fnameout = f'{basename}_{message["series_id"]:06d}_log.txt'
            path = os.path.join(outDirTiff, fnameout)
            with open(path,'a') as f:
                for key, value in message2.items():
                    if key != 'channels':
                        f.write(f'{key} {value}\n')
#                for channel in message2["channels"]:
#                    f.write(f'lost_pixel_count= {channel["lost_pixel_count"]} in threshold {channel["thresholds"]} \n')

# dump pixel mask and ff
        files=glob.glob(os.path.join(outDir,f'{basename}_s{message["series_id"]:06d}_metaData.cbor'))  
        for fname in files:
            with open(fname, 'rb') as f:
                message2 = cbor2.loads(f.read(), tag_hook=tag_hook)        
    
            log.info(f'**** dump pixel mask')    
            fname2 = f'{basename}_s{message["series_id"]:06d}_metaData.tif'
            path = os.path.join(outDirTiff, fname2)
            imgMap = message2["pixel_mask"]
            for i in imgMap.keys():
                imgName = path.replace('.tif',f'_mask_{i}.tif')
                tifffile.imsave(imgName, imgMap.get(i))
                
            log.info(f'**** dump flatfield')    
            fname2 = f'{basename}_s{message["series_id"]:06d}_metaData.tif'
            path = os.path.join(outDirTiff, fname2)
            imgMap = message2["flatfield"]
            for i in imgMap.keys():
                imgName = path.replace('.tif',f'_FF_{i}.tif')
                tifffile.imsave(imgName, imgMap.get(i))                                        
        
            log.info(f'**** dump start message in txt')             
            fname2 = f'{basename}_s{message["series_id"]:06d}_metaData.txt'
            path = os.path.join(outDirTiff, fname2)
            with open(path,'w') as f:
                for key, value in message2.items():
                    f.write(f'{key} {value}\n')
                    
        te2=time.perf_counter()
        print('at end2 = ',te2)
        
    
    elif message["type"] == "image":
        fname = f'{basename}_{message["series_id"]:06d}_{message["image_id"]:06d}.cbor'
        path = os.path.join(outDir, fname)
        with open(path, 'wb') as f:
            f.write(frame)
#    ti=time.perf_counter()
#    print(ti)        
            

def processFile(fname, outDir, basename=None): 
    with open(fname, 'rb') as f:
        message = cbor2.loads(f.read(), tag_hook=tag_hook)
    
    os.makedirs(outDir, exist_ok=True)
    if basename is None:
        basename = message["series_unique_id"]
#series_number->series_id
    if message["type"] == "start":
        log.info(f'proocess series {basename} {message["series_id"]}')
        fname = f'{basename}_s{message["series_id"]:06d}_metaData.txt'
        path = os.path.join(outDir, fname)
        with open(path, 'w') as f:
            for key, value in message.items():
                f.write(f'{key} {value}\n')
    
    elif message["type"] == "end":
        log.info(f'proocess end of series {message["series_unique_id"]} {message["series_id"]}')
    
    elif message["type"] == "image":
        fname = f'{basename}_{message["series_id"]:06d}_{message["image_id"]:06d}.tif'
        path = os.path.join(outDir, fname)
    
        for threshold, data in message["data"].items():
            imgName = path.replace('.tif', f'_{threshold}.tif')
            tifffile.imsave(imgName, data)       
            log.info(f'wrote {imgName}')               
        
#        for channel in message["channels"]:
#            channel["data"] = decompress_channel_data(channel)  
#            thresholds = "_".join(map(str, channel["thresholds"]))  
#            imgName = path.replace('.tif', f'_{thresholds}.tif')
#            tifffile.imsave(imgName, channel["data"])       
#            log.info(f'wrote {imgName}')     
