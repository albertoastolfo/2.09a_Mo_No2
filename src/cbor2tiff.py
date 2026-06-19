# 2022/12/8
# usage: python cbor2tiff.py -i inputdir -o outputdir
# scan inputdir directory to search .cbor file
# if it is image file, convert _threshold_1.tif and _threshold_2.tif
# if it is start metadata, convert _FF_threshold_1.tif, _FF_threshold_2.tif,
# _mask_threshold_1.tif, _mask_threshold_2.tif, _metaData.txt
# on outputdir directory
#
import cbor2
from dectris.compression import decompress
import numpy as np
import argparse, logging, os
import tifffile,glob
import os

logging.basicConfig()
log = logging.getLogger(__name__)


def parseArgs():
    parser = argparse.ArgumentParser(description = "comvert cbor file to tiff")
    parser.add_argument("-i", "--input", help="input file name", type=str, required=True)
    parser.add_argument("-o", "--outd", help="output file directory", type=str)
    args = parser.parse_args()
    return args

def get_unique_filename(path):
    base, ext = os.path.splitext(path)
    counter = 1

    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base}_{counter}{ext}"
        counter += 1

    return new_path


def subset_mydecoder_tif(path, output_path, output_name = 'image', stack_average = 0, th_difference = 0):
    
    #roi_y and roi_x should be [start_index, end_index] Python format (i.e. zero indexing)
    # to avoid saving one folder inside
    file_in = path +'\\'

    outDir = output_path
    
    #full is y = 512 and x = 1028
    #roi_y = np.array([0,512])
    #roi_x = np.array([0,1028])
    
    roi_y = np.array([0,210])
    roi_x = np.array([520,960])
    
    
    
    #roi_y = np.array([0,256])
    #roi_x = np.array([465,850])

    # this is the default name for the temporary files created in the "E:\EIGER_DATA" folder
    #filename = 'EIGER-TMP'

    #files=glob.glob(os.path.join(file_in, filename + '*.cbor')) 
    files=glob.glob(os.path.join(file_in, '*.cbor')) 
    

    # I cannot find a way to understand if it is dual energy or not in advance...
    # here I assueme it is not unless otherwise later
    is_dual_energy = 0
    Ny = roi_y[1] - roi_y[0]
    Nx = roi_x[1] - roi_x[0]
    
    if len(files) != 0:
          
        No_frames = len(files)-1
        
        #matrix = np.zeros((No_frames,512,1028,2))
        matrix_low = np.zeros((No_frames,Ny,Nx),dtype=np.uintc)
        matrix_high = np.zeros((No_frames,Ny,Nx),dtype=np.uintc)
        
        counter = 0
        
        for fname in files:    
            a=os.path.basename(fname)
            b=os.path.splitext(a)[0]
            c=b[:-14]
            basename=c
    #    path.basename is filename
    #    split .cbor
    #    prefix is _000000_000000: 14
        
            # print(a,b,basename)
        
            with open(fname, 'rb') as f:
                message = cbor2.loads(f.read(), tag_hook=tag_hook)
                
                # for threshold, data in message["start"].items():
                #     print(threshold)
                
                if message["type"] == "start":
                    fnametif = f'{basename}_{message["series_id"]:06d}_metaData.tif'
                elif message["type"] == "image":
                    fnametif = f'{basename}_{message["series_id"]:06d}_{message["image_id"]:06d}.tif'  
    #            print(fnametif)
                path2 = os.path.join(outDir, fnametif)
                os.makedirs(outDir, exist_ok=True)

            if message["type"] == "image":
            
                #g = message["data"].items()
    #        for channel in message["channels"]:
                for threshold, data in message["data"].items():
    #            channel["data"] = decompress_channel_data(channel)  
    #            thresholds = "_".join(map(str, channel["thresholds"])) 
                    
                    #print(threshold[-1])
                    if threshold[-1] == '1':
                       matrix_low[counter,:,:] = data[roi_y[0]:roi_y[1],roi_x[0]:roi_x[1]] 
                    if threshold[-1] == '2':
                        is_dual_energy = 1
                        matrix_high[counter,:,:] = data[roi_y[0]:roi_y[1],roi_x[0]:roi_x[1]] 
                        #matrix[counter,:,:,int(threshold[-1])-1] = data
                    
                
                counter = counter + 1
                    
                    # imgName = path2.replace('.tif', f'_{threshold}.tif')
                    # tifffile.imsave(imgName, data)
                    # log.info(f'wrote {imgName}')        

        # saving the stacks here:
        
            
        
        
        #print(path2)
        
        # for i in range(2):
        #     imgName = path2.replace('_metaData.tif', '_threshold_'+str(i+1)+'.tif')
        #     print(imgName)
        #     tifffile.imsave(imgName, matrix[:,:,:,i])

        #imgName_low = path2.replace('_metaData.tif', '_threshold_1.tif').replace(filename,output_name)
        #imgName_high = path2.replace('_metaData.tif', '_threshold_2.tif').replace(filename,output_name)
        imgName_low = os.path.join(outDir, output_name+'_th_1.tif')
        imgName_high = os.path.join(outDir, output_name+'_th_2.tif')
        
        #print(imgName_low.replace(filename,output_name))
        
        if th_difference == 0:
            if stack_average == 0:
                tifffile.imsave(imgName_low, matrix_low)
                if is_dual_energy:
                    tifffile.imsave(imgName_high, matrix_high)
            else:
                tifffile.imsave(imgName_low, np.float32(np.average(matrix_low,axis=0)))
                if is_dual_energy:
                    tifffile.imsave(imgName_high, np.float32(np.average(matrix_high,axis=0)))            
        else:
            #imgName_difference = path2.replace('_metaData.tif', '_threshold_difference.tif').replace(filename,output_name)
            imgName_difference = os.path.join(outDir, output_name+'_th_difference.tif')
            if stack_average == 0:
                tifffile.imsave(imgName_difference,matrix_low-matrix_high)
            else:
                tifffile.imsave(imgName_difference, np.float32(np.average(matrix_low-matrix_high,axis=0)))
        #return matrix_low
    
    else:
        print('File not found.')

def lastframe2tif(path = r'D:\EIGER_DATA', output_path = r'D:\EIGER_DATA', output_name = 'last.tif'):
    
    try:
        #roi_y and roi_x should be [start_index, end_index] Python format (i.e. zero indexing)
        # to avoid saving one folder inside
        file_in = path +'\\'

        outDir = output_path
        
        #full is y = 512 and x = 1028
        roi_y = np.array([0,512])
        roi_x = np.array([0,1028])
        

        # this is the default name for the temporary files created in the "E:\EIGER_DATA" folder
        #filename = 'EIGER-TMP'

        #files=glob.glob(os.path.join(file_in, filename + '*.cbor')) 
        files=glob.glob(os.path.join(file_in, '*.cbor')) 
        

        # I cannot find a way to understand if it is dual energy or not in advance...
        # here I assueme it is not unless otherwise later
        is_dual_energy = 0
        Ny = roi_y[1] - roi_y[0]
        Nx = roi_x[1] - roi_x[0]
        
        if len(files) != 0:
            
            No_frames = len(files)-1
            
            matrix = np.zeros((Ny,Nx),dtype=np.uintc)

            counter = 0
            
            #for fname in files[-2]:
            fname = files[-2]
            #print(fname) 
            a=os.path.basename(fname)
            b=os.path.splitext(a)[0]
            c=b[:-14]
            basename=c

        
            #print(a,b,basename)
        
            with open(fname, 'rb') as f:
                message = cbor2.loads(f.read(), tag_hook=tag_hook)

                
                if message["type"] == "start":
                    fnametif = f'{basename}_{message["series_id"]:06d}_metaData.tif'
                elif message["type"] == "image":
                    fnametif = f'{basename}_{message["series_id"]:06d}_{message["image_id"]:06d}.tif'  
                path2 = os.path.join(outDir, fnametif)
                os.makedirs(outDir, exist_ok=True)

            if message["type"] == "image":
            
                for threshold, data in message["data"].items():
                    if threshold[-1] == '1':
                        matrix[:,:] = data[roi_y[0]:roi_y[1],roi_x[0]:roi_x[1]]
            

            imgName = os.path.join(outDir, output_name)

            
            # I save only the low energy
            tifffile.imsave(imgName, matrix)
            
        else:
            print('File not found.')
    except:
        pass


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

def decode_dectris_compression(tag):
    algorithm, elem_size, encoded = tag.value
    return decompress(encoded, algorithm, elem_size=elem_size)

def decode_typed_array(tag, dtype):
    if not isinstance(tag.value, bytes):
        raise cbor2.CBORDecodeValueError("expected byte string in typed array")
    return np.frombuffer(tag.value, dtype=dtype)


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
    elem_size = {"uint8": 1, "uint16le": 2, "uint32le": 4}[data_type]

    if compression == "bslz4":
        decompressed = decompress(encoded, "bslz4-h5", elem_size=elem_size)
    elif compression == "lz4":
        decompressed = decompress(encoded, "lz4-h5")
    elif compression == "none":
        decompressed = encoded
    else:
        raise NotImplementedError(f"unknown compression: {compression}")

    return np.frombuffer(decompressed, dtype=dtype).reshape(dimensions)


def decoder_tif(file_in, file_out=None):
    
    file_in = file_in + '\\'
    
    outDir=file_out
    
    if file_out==None:
        outDir=os.path.dirname(file_in)
    
#    print(file_in, outDir)
    
    files=glob.glob(os.path.join(file_in,f'*.cbor')) 
    
    for fname in files:    
        a=os.path.basename(fname)
        b=os.path.splitext(a)[0]
        c=b[:-14]
        basename=c
#    path.basename is filename
#    split .cbor
#    prefix is _000000_000000: 14
    
#        print(a,b,basename)
    
        with open(fname, 'rb') as f:
            message = cbor2.loads(f.read(), tag_hook=tag_hook)
            if message["type"] == "start":
                fnametif = f'{basename}_{message["series_id"]:06d}_metaData.tif'
            elif message["type"] == "image":
                fnametif = f'{basename}_{message["series_id"]:06d}_{message["image_id"]:06d}.tif'  
#            print(fnametif)
            path2 = os.path.join(outDir, fnametif)
            os.makedirs(outDir, exist_ok=True)
    
        if message["type"] == "start":
            log.info(f'process series {message["series_id"]}')
            
            log.info(f'**** dump pixel mask')    
            path3 = os.path.join(outDir, fnametif)
            imgMap = message["pixel_mask"]
            for i in imgMap.keys():
                imgName = path3.replace('.tif',f'_mask_{i}.tif')
                tifffile.imwrite(imgName, imgMap.get(i))
                
            log.info(f'**** dump flatfield')    
            path3 = os.path.join(outDir, fnametif)
            imgMap = message["flatfield"]
            for i in imgMap.keys():
                imgName = path3.replace('.tif',f'_FF_{i}.tif')
                tifffile.imwrite(imgName, imgMap.get(i))                                        
        
            log.info(f'**** dump start message in txt')             
            fnametxt = f'{basename}_s{message["series_id"]:06d}_metaData.txt'
            path = os.path.join(outDir, fnametxt)
            with open(path,'w') as f:
                for key, value in message.items():
                    f.write(f'{key} {value}\n')  
        
        elif message["type"] == "image":
        
#        for channel in message["channels"]:
            for threshold, data in message["data"].items():
#            channel["data"] = decompress_channel_data(channel)  
#            thresholds = "_".join(map(str, channel["thresholds"]))  
                imgName = path2.replace('.tif', f'_{threshold}.tif')
                tifffile.imwrite(imgName, data)
                log.info(f'wrote {imgName}')


def mydecoder_tif(path, output_path, output_name = 'image', stack_average = 0):
    
    # to avoid saving one folder inside
    file_in = path +'\\'

    outDir = output_path

    # this is the default name for the temporary files created in the "E:\EIGER_DATA" folder
    #filename = 'EIGER-TMP'
    filename = ''


    files=glob.glob(os.path.join(file_in, filename + '*.cbor')) 
    
    print(files)


    # I cannot find a way to understand if it is dual energy or not in advance...
    # here I assueme it is not unless otherwise later
    is_dual_energy = 0
    
    if len(files) != 0:
          
        No_frames = len(files)-1
        
        #matrix = np.zeros((No_frames,512,1028,2))
        matrix_low = np.zeros((No_frames,512,1028),dtype=np.uintc)
        matrix_high = np.zeros((No_frames,512,1028),dtype=np.uintc)
        
        counter = 0
        
        for fname in files:    
            a=os.path.basename(fname)
            b=os.path.splitext(a)[0]
            c=b[:-14]
            basename=c
    #    path.basename is filename
    #    split .cbor
    #    prefix is _000000_000000: 14
        
            # print(a,b,basename)
        
            with open(fname, 'rb') as f:
                message = cbor2.loads(f.read(), tag_hook=tag_hook)
                
                # for threshold, data in message["start"].items():
                #     print(threshold)
                
                if message["type"] == "start":
                    fnametif = f'{basename}_{message["series_id"]:06d}_metaData.tif'
                elif message["type"] == "image":
                    fnametif = f'{basename}_{message["series_id"]:06d}_{message["image_id"]:06d}.tif'  
    #            print(fnametif)
                path2 = os.path.join(outDir, fnametif)
                os.makedirs(outDir, exist_ok=True)

            if message["type"] == "image":
            
                #g = message["data"].items()
    #        for channel in message["channels"]:
                for threshold, data in message["data"].items():
    #            channel["data"] = decompress_channel_data(channel)  
    #            thresholds = "_".join(map(str, channel["thresholds"])) 
                    
                    #print(threshold[-1])
                    if threshold[-1] == '1':
                       matrix_low[counter,:,:] = data 
                    if threshold[-1] == '2':
                        is_dual_energy = 1
                        matrix_high[counter,:,:] = data 
                        #matrix[counter,:,:,int(threshold[-1])-1] = data
                    
                
                counter = counter + 1
                    
                    # imgName = path2.replace('.tif', f'_{threshold}.tif')
                    # tifffile.imsave(imgName, data)
                    # log.info(f'wrote {imgName}')        

        # saving the stacks here:
        
        
        # for i in range(2):
        #     imgName = path2.replace('_metaData.tif', '_threshold_'+str(i+1)+'.tif')
        #     print(imgName)
        #     tifffile.imsave(imgName, matrix[:,:,:,i])

        #imgName_low = path2.replace('_metaData.tif', '_threshold_1.tif')#.replace(filename,output_name)
        #imgName_high = path2.replace('_metaData.tif', '_threshold_2.tif')#.replace(filename,output_name)

        #imgName_low = outDir + '/' + output_name + '_threshold_1.tif'
        #imgName_high = outDir + '/' + output_name + '_threshold_2.tif'


        imgName_low = os.path.join(outDir, output_name + '_Th_1.tif')
        imgName_high = os.path.join(outDir, output_name + '_Th_2.tif')

        # ensure unique filenames
        imgName_low = get_unique_filename(imgName_low)
        imgName_high = get_unique_filename(imgName_high)


        #print(imgName_low.replace(filename,output_name))
        

        if stack_average == 0:
            tifffile.imsave(imgName_low, matrix_low)
            if is_dual_energy:
                tifffile.imsave(imgName_high, matrix_high)
        else:
            tifffile.imsave(imgName_low, np.float32(np.average(matrix_low,axis=0)))
            if is_dual_energy:
                tifffile.imsave(imgName_high, np.float32(np.average(matrix_high,axis=0)))            

        #return matrix_low
    
    else:
        print('File not found.')

def decoder_tif_khush(file_in, file_out=None, output_name = 'image'):
    
    file_in = file_in + '\\'
    
    outDir=file_out
    
    if file_out==None:
        outDir=os.path.dirname(file_in)
    
#    print(file_in, outDir)
    
    files=glob.glob(os.path.join(file_in,f'*.cbor')) 
    
    for fname in files:    
        a=os.path.basename(fname)
        b=os.path.splitext(a)[0]
        c=b[:-14]
        # basename=c
        basename=output_name
#    path.basename is filename
#    split .cbor
#    prefix is _000000_000000: 14
    
#        print(a,b,basename)
    
        with open(fname, 'rb') as f:
            message = cbor2.loads(f.read(), tag_hook=tag_hook)
            if message["type"] == "start":
                fnametif = f'{basename}_{message["series_id"]:06d}_metaData.tif'
            elif message["type"] == "image":
                fnametif = f'{basename}_{message["series_id"]:06d}_{message["image_id"]:06d}.tif'  
#            print(fnametif)
            path2 = os.path.join(outDir, fnametif)
            os.makedirs(outDir, exist_ok=True)
    
        if message["type"] == "start":
            log.info(f'process series {message["series_id"]}')
            
            log.info(f'**** dump pixel mask')    
            path3 = os.path.join(outDir, fnametif)
            imgMap = message["pixel_mask"]
            for i in imgMap.keys():
                imgName = path3.replace('.tif',f'_mask_{i}.tif')
                tifffile.imwrite(imgName, imgMap.get(i))
                
            log.info(f'**** dump flatfield')    
            path3 = os.path.join(outDir, fnametif)
            imgMap = message["flatfield"]
            for i in imgMap.keys():
                imgName = path3.replace('.tif',f'_FF_{i}.tif')
                tifffile.imwrite(imgName, imgMap.get(i))                                        
        
            log.info(f'**** dump start message in txt')             
            fnametxt = f'{basename}_s{message["series_id"]:06d}_metaData.txt'
            path = os.path.join(outDir, fnametxt)
            with open(path,'w') as f:
                for key, value in message.items():
                    f.write(f'{key} {value}\n')  
        
        elif message["type"] == "image":
        
#        for channel in message["channels"]:
            for threshold, data in message["data"].items():
#            channel["data"] = decompress_channel_data(channel)  
#            thresholds = "_".join(map(str, channel["thresholds"]))  
                imgName = path2.replace('.tif', f'_{threshold}.tif')
                tifffile.imwrite(imgName, data)
                log.info(f'wrote {imgName}')

if __name__=='__main__':
    args = parseArgs()
    decoder_tif(args.input, args.outd)
    print('decoding from cbor to tiff is done.')
    
    
    
