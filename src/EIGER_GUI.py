# -*- coding: utf-8 -*-
"""
Created on March 2026
@author: AAstolfo
"""

import tkinter
from tkinter import ttk, Tk, filedialog
import os
import threading
import time
import EIGER_functions as EIGER


class EIGER_GUI(ttk.Frame):
    """The GUI for using EIGER in a slightly more decent way."""

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent

        # Instance variables instead of globals
        self.live_running = False
        self.init_done = False
        self.triggers_sent = 0

        self.init_gui()

    def Quit(self):
        self.live_running = False
        self.root.destroy()

    def init_receiver(self):

        # to init the EIGER receiver
        EIGER.init_receiver()
        
        #pass

    def init(self):
        
        # to init the EIGER detector
        EIGER.init()
        self.init_done = True

        # after the initialization, set the exposure time and energy thresholds to the values in the GUI
        if self.init_done:
            EIGER.set_exposure_time(float(self.EXPOSURE_TIME_display.cget('text')))
            #print(self.ENERGY_THRESHOLDS_display.cget('text'))
            #EIGER.set_thresholds(self.ENERGY_THRESHOLDS_display.cget('text'))
            thresholds_display_text = self.ENERGY_THRESHOLDS_display.cget('text')
            #th1, th2 = thresholds_display_text.split(',')
            th1, th2 = (thresholds_display_text.split(',') + [None, None])[:2]
            if th2 == None:
                EIGER.set_thresholds(float(th1))
            else:
                if len(th1) > 0 and len(th2) > 0:
                    EIGER.set_thresholds(float(th1), float(th2))
                

    def snap(self):
        
        #take a snap and save it on the saving folder with the current settings of the GUI (exposure time, energy thresholds, number of images)

        if self.init_done:
            path = self.SAVING_PATH_display.cget('text')
            
            # before taking the snap, set the exposure time and energy thresholds to the values in the GUI
            EIGER.set_exposure_time(float(self.EXPOSURE_TIME_display.cget('text')))
            #print(self.ENERGY_THRESHOLDS_display.cget('text'))
            thresholds_display_text = self.ENERGY_THRESHOLDS_display.cget('text')
            #th1, th2 = thresholds_display_text.split(',')
            th1, th2 = (thresholds_display_text.split(',') + [None, None])[:2]
            if th2 == None:
                EIGER.set_thresholds(float(th1))
            else:
                if len(th1) > 0 and len(th2) > 0:
                    EIGER.set_thresholds(float(th1), float(th2))
            #EIGER.set_thresholds(self.ENERGY_THRESHOLDS_display.cget('text'))

            EIGER.snap(path)
        else:
            print("Please initialize the detector first by clicking 'INIT'.")
        
        
        
        #pass

    def init_live(self):
        # Run BAT file in background so GUI doesn't freeze
        threading.Thread(
            target=lambda: os.system(r'C:\Python\2.09a_Mo_No2\src\run_live_EIGER.bat'),
            daemon=True
        ).start()

        # Start the live loop
        #self.start_live()

    def start_live(self):
        if not self.live_running:
            self.live_running = True
            print("Live started")
            self.triggers_sent == 0
            # before starting the live loop, set the exposure time and energy thresholds to the values in the GUI
            if self.init_done:
                EIGER.set_exposure_time(float(self.EXPOSURE_TIME_display.cget('text')))
                #EIGER.set_thresholds(self.ENERGY_THRESHOLDS_display.cget('text'))
                
                thresholds_display_text = self.ENERGY_THRESHOLDS_display.cget('text')
                th1, th2 = (thresholds_display_text.split(',') + [None, None])[:2]
                #th1, th2 = thresholds_display_text.split(',')
                if th2 == None:
                    EIGER.set_thresholds(float(th1))
                else:
                    if len(th1) > 0 and len(th2) > 0:
                        EIGER.set_thresholds(float(th1), float(th2))


            # Start background thread
            threading.Thread(target=self.live_loop, daemon=True).start()

    def stop_live(self):
        self.live_running = False

        EIGER.disarm()
        self.triggers_sent = 0

        print("Live stopped")

    def live_loop(self):
        """Runs in a background thread — never blocks the GUI."""
        while self.live_running:
            print('trigger sent:', self.triggers_sent)
            if self.triggers_sent ==0 or self.triggers_sent == 10:
                #I set the detector for a live acquisition (I don't want to overload the detector/folder so I got for 100 at a time)
                self.triggers_sent = 0 
                EIGER.set_nimages_ntriggers(1, 10)
                EIGER.arm()

                time.sleep(0.1)  # Safe because it's in a thread
                
                
                EIGER.trigger(0)
                self.triggers_sent += 1
                time.sleep(1)  # Safe because it's in a thread
                print("trigger")  # Your live action here
            else:
                if self.triggers_sent ==9 :
                    EIGER.trigger(1)
                    time.sleep(1) 
                    print("trigger sent 10, waiting for acquisition to finish...")
                    self.triggers_sent = 0 
                else:
                    EIGER.trigger(0)
                    self.triggers_sent += 1

            # If you need to update GUI, do it safely:
            # self.root.after(0, lambda: self.SOME_LABEL.config(text="updated"))

            #time.sleep()  # Safe because it's in a thread

    def update_path(self):
        root = Tk()
        root.withdraw()
        open_file = filedialog.askdirectory()
        self.SAVING_PATH_display.config(text=open_file)

    def update_entry(self, in_text, out_text):
        user_entry = in_text.get()
        try:
            if out_text == self.ENERGY_THRESHOLDS_display:
                points = user_entry.split(',')
                if len(points) < 3:
                    for point in points:
                        float(point)
                    out_text.config(text=user_entry)

            if out_text == self.NO_IMAGES_display:
                check = int(in_text.get())
                if 0 < check < 1000:
                    out_text.config(text=user_entry)

            if out_text == self.EXPOSURE_TIME_display:
                check = float(in_text.get())
                if 0.01 <= check <= 10:
                    out_text.config(text=float(user_entry))

        except:
            print('error message')

    def init_gui(self):
        self.root.title('AXIm EIGER GUI')
        self.root.option_add('*tearOff', 'FALSE')

        self.grid(column=0, sticky='nsew')

        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menu_file.add_command(label='Quit', command=self.Quit)
        self.root.config(menu=self.menubar)

        self.INIT_RECEIVER_button = ttk.Button(self, text="INIT RECEIVER", command=self.init_receiver)
        self.INIT_button = ttk.Button(self, text="INIT DETECTOR", command=self.init)
        self.SNAP_button = ttk.Button(self, text="SNAP", command=self.snap)
        self.INIT_LIVE_button = ttk.Button(self, text="INIT LIVE", command=self.init_live)
        self.START_LIVE_button = ttk.Button(self, text="START LIVE", command=self.start_live)
        self.STOP_LIVE_button = ttk.Button(self, text="STOP LIVE", command=self.stop_live)

        self.SAVING_PATH_button = ttk.Button(self, text="SET snap image saving path", command=self.update_path)
        self.SAVING_PATH_display = ttk.Label(self, text="D:\\EIGER_DATA\\GUI_DEFAULT")

        self.ENERGY_THRESHOLDS_label = ttk.Label(self, text="Energy Thresholds [keV]")
        self.ENERGY_THRESHOLDS_entry = ttk.Entry(self)
        self.ENERGY_THRESHOLDS_button = ttk.Button(self, text="SET",
                                                   command=lambda: self.update_entry(self.ENERGY_THRESHOLDS_entry,
                                                                                     self.ENERGY_THRESHOLDS_display))
        self.ENERGY_THRESHOLDS_display = ttk.Label(self, text="10,20")

        self.EXPOSURE_TIME_label = ttk.Label(self, text="Exposure time [s]")
        self.EXPOSURE_TIME_entry = ttk.Entry(self)
        self.EXPOSURE_TIME_button = ttk.Button(self, text="SET",
                                               command=lambda: self.update_entry(self.EXPOSURE_TIME_entry,
                                                                                 self.EXPOSURE_TIME_display))
        self.EXPOSURE_TIME_display = ttk.Label(self, text="1.0")

        self.NO_IMAGES_label = ttk.Label(self, text="Number of images")
        self.NO_IMAGES_entry = ttk.Entry(self)
        self.NO_IMAGES_button = ttk.Button(self, text="SET",
                                           command=lambda: self.update_entry(self.NO_IMAGES_entry,
                                                                             self.NO_IMAGES_display))
        self.NO_IMAGES_display = ttk.Label(self, text="10")

        # Layout
        self.INIT_RECEIVER_button.grid(row=0, column=0)
        self.INIT_button.grid(row=0, column=1)

        self.EXPOSURE_TIME_label.grid(row=2, column=0)
        self.EXPOSURE_TIME_entry.grid(row=2, column=1)
        self.EXPOSURE_TIME_button.grid(row=2, column=2)
        self.EXPOSURE_TIME_display.grid(row=3, column=0, columnspan=3)

        self.ENERGY_THRESHOLDS_label.grid(row=6, column=0)
        self.ENERGY_THRESHOLDS_entry.grid(row=6, column=1)
        self.ENERGY_THRESHOLDS_button.grid(row=6, column=2)
        self.ENERGY_THRESHOLDS_display.grid(row=7, column=0, columnspan=3)

        self.NO_IMAGES_label.grid(row=10, column=0)
        self.NO_IMAGES_entry.grid(row=10, column=1)
        self.NO_IMAGES_button.grid(row=10, column=2)
        self.NO_IMAGES_display.grid(row=11, column=0, columnspan=3)

        self.SAVING_PATH_button.grid(row=12, column=0)
        self.SAVING_PATH_display.grid(row=13, column=0, columnspan=3)

        self.INIT_LIVE_button.grid(row=0, column=3)
        self.START_LIVE_button.grid(row=1, column=3)
        self.STOP_LIVE_button.grid(row=2, column=3)

        for child in self.winfo_children():
            child.grid_configure(padx=6, pady=6)


if __name__ == '__main__':
    root = tkinter.Tk()
    EIGER_GUI(root)
    root.mainloop()