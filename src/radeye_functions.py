# -*- coding: utf-8 -*-

# this is a tentative file for the radeye functions

import numpy as np
import os
import subprocess
import time
import imageio.v3 as iio
#from glob import glob
import glob
import shutil


data_path = r"C:\ProgramData\Teledyne DALSA\DATA"
output_path_default = r"C:\Users\AXIm Admin\Downloads\average_image.tiff"

def run_cmd_function(No_frames=5, sum_frames = 0):
    """
    Function to run a command to grab images from a camera.
    :param No_frames: Number of frames to grab.

    this will save the images on the fixed folder C:\ProgramData\Teledyne DALSA\DATA as the C++ code is set to do so.
    The function will delete any existing .raw files in the specified data_path before running the command
    """
    # Define the path to the executable
    exe_path = r"C:\Program Files\Teledyne DALSA\Sapera\Examples\Classes\GrabConsole_save_average_2\Vc\Debug64\GrabCPP.exe"
    
    # Only delete .raw files before running the command
    #raw_files = glob.glob(os.path.join(data_path, "*.raw"))

    #for file in raw_files:
    #    os.remove(file)

    # Run the command with the specified number of frames
    if sum_frames:
        subprocess.run([exe_path, str(No_frames), "--sum"], shell=True)
    else:    
        subprocess.run([exe_path, str(No_frames)], shell=True)

    return 0

def average_frames(output_path = output_path_default, folder_path = r"C:\ProgramData\Teledyne DALSA\DATA", width=10720, height=8064):
    """
    Function to average raw image files in a specified folder and save the result.
    
    :param folder_path: Path to the folder containing raw image files.
    :param output_path: Path where the averaged image will be saved.
    :param width: Width of the images.
    :param height: Height of the images.
    """
    # Find raw files
    raw_files = glob.glob(os.path.join(folder_path, "*.raw"))
    num_files = len(raw_files)

    if num_files == 0:
        print("No raw files found.")
        return

    # Preallocate accumulator
    accumulator = np.zeros((height, width), dtype=np.float32)

    # Loop efficiently
    for file in raw_files:
        with open(file, "rb") as f:
            img = np.frombuffer(f.read(), dtype=np.uint16).reshape((height, width))
            accumulator += img

    # Compute average
    average_img = accumulator / num_files

    # Save result
    iio.imwrite(output_path, average_img.astype(np.float32), extension=".tiff")
    
    print(f"Saved average image to: {output_path}")

def convert_raw_to_tiff(raw_file, output_file):
    """
    Function to convert a raw image file to TIFF format.
    
    :param raw_file: Path to the raw image file.
    :param output_file: Path where the TIFF image will be saved.
    """
    img = np.fromfile(raw_file, dtype=np.float32)
    img = img.reshape((8064, 10720))  # Adjust dimensions as needed
    iio.imwrite(output_file, img.astype(np.float32), extension=".tiff")
    print(f"Converted {raw_file} to {output_file}")


def snap(No_frames=5, output_path=output_path_default,sum_frames = 0):
    #"""
    #Function to grab images and compute their average.
    
    #:param No_frames: Number of frames to grab.
    #:param output_path: Path where the averaged image will be saved.
#
    #call is as follows:
    #snap(10, r"C:\Users\AXIm Admin\Downloads\test.tiff",1)
    #"""
    #run_cmd_function(No_frames)
    if sum_frames:
        run_cmd_function(No_frames, sum_frames=1)

        convert_raw_to_tiff(os.path.join(data_path, "SumFrame32.raw"), output_path)
        print(f"Saved summed image to: {output_path}")
        # copy the raw files to the output path with a new name
        #shutil.copy(os.path.join(data_path, "SumFrame32.raw"), output_path)
        #print(f"Saved summed image to: {output_path}")
    else:
        run_cmd_function(No_frames, sum_frames=0)
        average_frames(output_path)

#t00 = time.time()
#snap(10, r"C:\Users\AXIm Admin\Downloads\testone.tiff",1)
#print("Time taken:", time.time() - t00)
