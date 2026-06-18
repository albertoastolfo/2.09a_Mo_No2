# $env:SCYJAVA_NO_CJDK = "1"
# $env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-8.0.482.8-hotspot"
# $env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

import imagej
import time
import pathlib
import numpy as np
import jpype
import cbor2tiff as c2t

# Start ImageJ with ImageJ1 enabled
ij = imagej.init(mode='interactive', add_legacy=True)
ij.ui().showUI()

# Import ImageJ1 classes
ImagePlus = jpype.JClass('ij.ImagePlus')
IJ = jpype.JClass('ij.IJ')

watch_folder = pathlib.Path(r"D:\EIGER_DATA")
#extensions = {".tif", ".tiff", ".png", ".jpg", ".jpeg", ".cbor"}
extensions = {".jpg",".cbor"}

last_seen = None
imp = None  # ImagePlus window

title= "Live Viewer"

while True:

    
    images = [f for f in watch_folder.iterdir() if f.suffix.lower() in extensions]
    #print(images)
    if images:
        newest = max(images, key=lambda f: f.stat().st_mtime)
        #print(f"newest : {newest}")
        if newest != last_seen:
            
            
            print(f"Updating: {newest.name}")
            # I run the conversion of the last tif in cbor
            c2t.lastframe2tif()

            # Load new image as ImagePlus (ImageJ1)
            #new_imp = IJ.openImage(str(newest))
            new_imp = IJ.openImage(r'D:\EIGER_DATA\last.tif')
            if imp is None:
                # First time: show the window
                imp = new_imp
                imp.setTitle(title)
                imp.show()
            else:
                # Replace pixel data
                old_pixels = imp.getProcessor().getPixels()
                new_pixels = new_imp.getProcessor().getPixels()

                # Copy new pixels into old buffer
                old_pixels[:] = new_pixels[:]

                # Refresh the window
                imp.updateAndDraw()
                imp.setTitle(title)

            last_seen = newest
            #print('last_seen = ', last_seen)

    time.sleep(1)