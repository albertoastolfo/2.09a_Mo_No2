# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 12:39:11 2022

@author: Alberto Astolfo
"""


import kohzu_functions_007Mo_No2 as KZ
import newport_functions as NP
import tkinter
from tkinter import ttk


class Mo007No2_GUI(ttk.Frame):
    #import Newport_functions
    """The motors GUI and functions."""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def update_positions(self):
        if initialised == 1:
            
            digits = 6
            
            #Check the status of the motors [Newport only]
            if NP_initialised == 1:
                try:
                    status1 = NP.get_status(1)
                    status3 = NP.get_status(2)
                    status5 = NP.get_status(3)
                    status7 = NP.get_status(4)
                    status8 = NP.get_status(5)
                    status11 = NP.get_status(6)
                except:
                    status1 = 0
                    status3 = 0
                    status5 = 0   
                    status7 = 0 
                    status8 = 0 
                    status11 = 0           
            
            
                # Check the positions and write 'Not connected' if the controller is not available
                try:
                    pos1 = NP.get_position(1)
                    if status1 > 10:
                        self.M1_pos.config(text=str(round(pos1,digits)))
                    else:
                        self.M1_pos.config(text='Status = '+str(status1))                    
                except:
                    pos1 = 'Not connected'
                    self.M1_pos.config(text=pos1)
    
                try:
                    pos3 = NP.get_position(2)
                    if status3 > 10:
                        self.M3_pos.config(text=str(round(pos3,digits)))
                    else:
                        self.M3_pos.config(text='Status = '+str(status3))                    
                except:
                    self.M3_pos.config(text='Not connected')    

                try:                
                    pos5 = NP.get_position(3)
                    if status5 > 10:
                        self.M5_pos.config(text=str(round(pos5,digits)))
                    else:
                        self.M5_pos.config(text='Status = '+str(status5))        
                except:
                    self.M5_pos.config(text='Not connected') 
        
                try:                
                    pos7 = NP.get_position(4)
                    if status7 > 10:
                        self.M7_pos.config(text=str(round(pos7,digits)))
                    else:
                        self.M7_pos.config(text='Status = '+str(status7))        
                except:
                    self.M7_pos.config(text='Not connected')

                try:                
                    pos8 = NP.get_position(5)
                    if status8 > 10:
                        self.M8_pos.config(text=str(round(pos8,digits)))
                    else:
                        self.M8_pos.config(text='Status = '+str(status8))        
                except:
                    self.M8_pos.config(text='Not connected') 
                
                try:                
                    pos11 = NP.get_position(6)
                    if status11 > 10:
                        self.M11_pos.config(text=str(round(pos11,digits)))
                    else:
                        self.M11_pos.config(text='Status = '+str(status11))        
                except:
                    self.M11_pos.config(text='Not connected') 

            # [Kohzu here]
            if KZ_initialised == 1:            
                #Check motors position (Kohzu)
                try:
                    pos2 = KZ.get_position(1,no_print=1)
                    self.M2_pos.config(text=str(round(pos2,digits)))
                except:
                    self.M2_pos.config(text='Not connected') 
                try:
                    pos4 = KZ.get_position(2,no_print=1)
                    self.M4_pos.config(text=str(round(pos4,digits)))
                except:
                    self.M4_pos.config(text='Not connected') 

                try:
                    pos6 = KZ.get_position(3,no_print=1)
                    self.M6_pos.config(text=str(round(pos6,digits)))
                except:
                    self.M6_pos.config(text='Not connected') 

                try:
                    pos10 = KZ.get_position(4,no_print=1)
                    self.M10_pos.config(text=str(round(pos10,digits)))
                except:
                    self.M10_pos.config(text='Not connected') 

                try:
                    pos12 = KZ.get_position(5,no_print=1)
                    self.M12_pos.config(text=str(round(pos12,digits)))
                except:
                    self.M12_pos.config(text='Not connected')
                    

        else:
            self.M1_pos.config(text='Not connected')
            self.M2_pos.config(text='Not connected')
            self.M3_pos.config(text='Not connected')
            self.M4_pos.config(text='Not connected')
            self.M5_pos.config(text='Not connected')
            self.M6_pos.config(text='Not connected')
            self.M7_pos.config(text='Not connected')
            self.M8_pos.config(text='Not connected')
            # self.M9_pos.config(text='Not connected')
            self.M10_pos.config(text='Not connected')
            self.M11_pos.config(text='Not connected')
            self.M12_pos.config(text='Not connected')
            
    def update_label(self):
        #self.label.configure(cpuTemp)
        #self.M1_pos.config(text='ciao')
        self.update_positions()
        self.M1_pos.after(1000,self.update_label)

    def Quit(self):
        
        if initialised == 1:
            self.sockets_close()
        
        self.root.destroy()


    def sockets_init(self):
        # initialise all the controllers
        
        global NP_sockets, initialised, NP_initialised, KZ_initialised, NPi_initialised
        
        try: 
            NP_sockets = NP.init()
            NP_initialised = 1
            
        except:
            NP_initialised = 0
            print("Newport not connected")
        try:
            #ser = KZ.init()
            KZ.init()
            KZ_initialised = 1
        #except:
        except Exception as e:
            KZ_initialised = 0
            print('Error is: ', e)
            print("Kohzu not connected")
            
        initialised = 1


    def sockets_close(self):
        # close all the controllers
        
        global NP_sockets, initialised, NP_initialised, KZ_initialised, NPi_initialised       
        
        if NP_initialised == 1:
            #try:
                NP.close()
                NP_initialised = 0
            #except:
            #    pass
        
        if KZ_initialised == 1:
            try:
                KZ.close()
                KZ_initialised = 0
            except:
                pass
        
        initialised = 0
        

    def init_gui(self):
        
        global initialised,NP_initialised,NPi_initialised,KZ_initialised
        
        """Builds GUI."""
        self.root.title('007-Mo #2 ALL-MOTORS')
        self.root.option_add('*tearOff', 'FALSE')

        self.grid(column=0, sticky='nsew')

        self.menubar = tkinter.Menu(self.root)

        self.menu_file = tkinter.Menu(self.menubar)
        #self.menu_file.add_command(label='Exit')

        self.menu_edit = tkinter.Menu(self.menubar)

        self.menubar.add_cascade(menu=self.menu_file, label='File')
        #self.menubar.add_cascade(menu=self.menu_edit, label='Edit')

        self.menu_file.add_command(label='Quit',command = lambda: self.Quit())

        self.root.config(menu=self.menubar)

        self.INIT_button = ttk.Button(self,text="INIT", command = self.sockets_init)
        self.QUIT_button = ttk.Button(self,text="CLOSE", command = self.sockets_close)

        self.INIT_button.grid(row = 16+8, column =2)
        self.QUIT_button.grid(row = 16+8, column =3)
    
    
        #-----MOTOR 1------
        MOTOR_No = 1
    
        self.M1_label_1 = ttk.Label(self,text = "Mask-X")
        self.M1_label_1.config(font='-weight bold')
        self.M1_pos = ttk.Label(self)
        self.M1_pos.after(1000,self.update_label)
        self.M1_label_1.grid(row = 0, column =1)
        self.M1_pos.grid(row=1,column =1)
        self.M1_label_2 = ttk.Label(self,text = "Move ABS [mm]")
        self.M1_Entry_1 = ttk.Entry(self)
        self.M1_label_3 = ttk.Label(self,text = "Move REL [mm]")
        self.M1_Entry_2 = ttk.Entry(self)
        
        self.M1_button_1 = ttk.Button(self,text="<", command = lambda: NP.move_relative(1,'-'+self.M1_Entry_2.get()))
        self.M1_button_2 = ttk.Button(self,text=">", command = lambda: NP.move_relative(1,self.M1_Entry_2.get()))
        self.M1_button_3 = ttk.Button(self,text="STOP", command = lambda: NP.stop(1))
        self.M1_button_4 = ttk.Button(self,text="HOME", command = lambda: NP.move_absolute(1,0))
        self.M1_button_5 = ttk.Button(self,text="GO", command = lambda: NP.move_absolute(1,self.M1_Entry_1.get()))
        
        self.M1_label_1.grid(row = 0, column =1+(MOTOR_No-1)*3)
        self.M1_pos.grid(row=1,column =1+(MOTOR_No-1)*3)
        self.M1_label_2.grid(row = 2, column =1+(MOTOR_No-1)*3)
        self.M1_Entry_1.grid(row = 3, column =1+(MOTOR_No-1)*3)
        self.M1_label_3.grid(row = 4, column =1+(MOTOR_No-1)*3)
        self.M1_Entry_2.grid(row = 5, column =1+(MOTOR_No-1)*3)
        self.M1_button_1.grid(row = 5, column =0+(MOTOR_No-1)*3)
        self.M1_button_2.grid(row = 5, column =2+(MOTOR_No-1)*3)
        self.M1_button_3.grid(row = 6, column =1+(MOTOR_No-1)*3)
        self.M1_button_4.grid(row = 7, column =1+(MOTOR_No-1)*3)
        self.M1_button_5.grid(row = 3, column =2+(MOTOR_No-1)*3)
        
        
        #-----MOTOR 2------
        MOTOR_No = 2
        self.M2_label_1 = ttk.Label(self,text = "Mask-Y")
        self.M2_label_1.config(font='-weight bold')
        self.M2_pos = ttk.Label(self,text = "0.0")
        
        self.M2_label_2 = ttk.Label(self,text = "Move ABS [mm]")
        self.M2_Entry_1 = ttk.Entry(self)
        
        self.M2_label_3 = ttk.Label(self,text = "Move REL [mm]")
        self.M2_Entry_2 = ttk.Entry(self)
        
        self.M2_button_1 = ttk.Button(self,text="<", command = lambda: KZ.move_relative(1,float('-'+self.M2_Entry_2.get())))
        self.M2_button_2 = ttk.Button(self,text=">", command = lambda: KZ.move_relative(1,float(self.M2_Entry_2.get())))
        self.M2_button_3 = ttk.Button(self,text="STOP", command = lambda: KZ.stop(1) )
        self.M2_button_4 = ttk.Button(self,text="HOME", command = lambda: KZ.home(1) )
        self.M2_button_5 = ttk.Button(self,text="GO", command = lambda: KZ.move_absolute(1,float(self.M2_Entry_1.get())))
        
        self.M2_label_1.grid(row = 0, column =1+(MOTOR_No-1)*3)
        self.M2_pos.grid(row=1,column =1+(MOTOR_No-1)*3)
        self.M2_label_2.grid(row = 2, column =1+(MOTOR_No-1)*3)
        self.M2_Entry_1.grid(row = 3, column =1+(MOTOR_No-1)*3)
        self.M2_label_3.grid(row = 4, column =1+(MOTOR_No-1)*3)
        self.M2_Entry_2.grid(row = 5, column =1+(MOTOR_No-1)*3)
        self.M2_button_1.grid(row = 5, column =0+(MOTOR_No-1)*3)
        self.M2_button_2.grid(row = 5, column =2+(MOTOR_No-1)*3)
        self.M2_button_3.grid(row = 6, column =1+(MOTOR_No-1)*3)
        self.M2_button_4.grid(row = 7, column =1+(MOTOR_No-1)*3)
        self.M2_button_5.grid(row = 3, column =2+(MOTOR_No-1)*3)


        # #-----MOTOR 3------
        MOTOR_No = 3
        self.M3_label_1 = ttk.Label(self,text = "Mask-Z")
        self.M3_label_1.config(font='-weight bold')
        self.M3_pos = ttk.Label(self,text = "0.0")
        
        self.M3_label_2 = ttk.Label(self,text = "Move ABS [mm]")
        self.M3_Entry_1 = ttk.Entry(self)
        
        self.M3_label_3 = ttk.Label(self,text = "Move REL [mm]")
        self.M3_Entry_2 = ttk.Entry(self)
        
        self.M3_button_1 = ttk.Button(self,text="<", command = lambda: NP.move_relative(2,'-'+self.M3_Entry_2.get()))
        self.M3_button_2 = ttk.Button(self,text=">", command = lambda: NP.move_relative(2,self.M3_Entry_2.get()))
        self.M3_button_3 = ttk.Button(self,text="STOP", command = lambda: NP.stop(2) )
        self.M3_button_4 = ttk.Button(self,text="HOME", command = lambda: NP.move_absolute(2,0) )
        self.M3_button_5 = ttk.Button(self,text="GO", command = lambda: NP.move_absolute(2,self.M3_Entry_1.get()))
        
        self.M3_label_1.grid(row = 0, column =1+(MOTOR_No-1)*3)
        self.M3_pos.grid(row=1,column =1+(MOTOR_No-1)*3)
        self.M3_label_2.grid(row = 2, column =1+(MOTOR_No-1)*3)
        self.M3_Entry_1.grid(row = 3, column =1+(MOTOR_No-1)*3)
        self.M3_label_3.grid(row = 4, column =1+(MOTOR_No-1)*3)
        self.M3_Entry_2.grid(row = 5, column =1+(MOTOR_No-1)*3)
        self.M3_button_1.grid(row = 5, column =0+(MOTOR_No-1)*3)
        self.M3_button_2.grid(row = 5, column =2+(MOTOR_No-1)*3)
        self.M3_button_3.grid(row = 6, column =1+(MOTOR_No-1)*3)
        self.M3_button_4.grid(row = 7, column =1+(MOTOR_No-1)*3)
        self.M3_button_5.grid(row = 3, column =2+(MOTOR_No-1)*3)

        # #-----MOTOR 4------
        MOTOR_No = 4
        self.M4_label_1 = ttk.Label(self,text = "Mask-ROTX")
        self.M4_label_1.config(font='-weight bold')
        self.M4_pos = ttk.Label(self,text = "0.0")
        
        self.M4_label_2 = ttk.Label(self,text = "Move ABS [deg]")
        self.M4_Entry_1 = ttk.Entry(self)
        
        self.M4_label_3 = ttk.Label(self,text = "Move REL [deg]")
        self.M4_Entry_2 = ttk.Entry(self)
        
        self.M4_button_1 = ttk.Button(self,text="<", command = lambda: KZ.move_relative(2,'-'+self.M4_Entry_2.get()))
        self.M4_button_2 = ttk.Button(self,text=">", command = lambda: KZ.move_relative(2,self.M4_Entry_2.get()))
        self.M4_button_3 = ttk.Button(self,text="STOP", command = lambda: KZ.stop(2) )
        self.M4_button_4 = ttk.Button(self,text="HOME", command = lambda: KZ.home(2) )
        self.M4_button_5 = ttk.Button(self,text="GO", command = lambda: KZ.move_absolute(2,self.M4_Entry_1.get()))
        
        self.M4_label_1.grid(row = 0, column =1+(MOTOR_No-1)*3)
        self.M4_pos.grid(row=1,column =1+(MOTOR_No-1)*3)
        self.M4_label_2.grid(row = 2, column =1+(MOTOR_No-1)*3)
        self.M4_Entry_1.grid(row = 3, column =1+(MOTOR_No-1)*3)
        self.M4_label_3.grid(row = 4, column =1+(MOTOR_No-1)*3)
        self.M4_Entry_2.grid(row = 5, column =1+(MOTOR_No-1)*3)
        self.M4_button_1.grid(row = 5, column =0+(MOTOR_No-1)*3)
        self.M4_button_2.grid(row = 5, column =2+(MOTOR_No-1)*3)
        self.M4_button_3.grid(row = 6, column =1+(MOTOR_No-1)*3)
        self.M4_button_4.grid(row = 7, column =1+(MOTOR_No-1)*3)
        self.M4_button_5.grid(row = 3, column =2+(MOTOR_No-1)*3)

        # #-----MOTOR 5------
        MOTOR_No = 5
        self.M5_label_1 = ttk.Label(self,text = "Mask-ROTY")
        self.M5_label_1.config(font='-weight bold')
        self.M5_pos = ttk.Label(self,text = "0.0")
        
        self.M5_label_2 = ttk.Label(self,text = "Move ABS [deg]")
        self.M5_Entry_1 = ttk.Entry(self)
        
        self.M5_label_3 = ttk.Label(self,text = "Move REL [deg]")
        self.M5_Entry_2 = ttk.Entry(self)
        
        
        self.M5_button_1 = ttk.Button(self,text="<", command = lambda: NP.move_relative(3,float('-'+self.M5_Entry_2.get())))
        self.M5_button_2 = ttk.Button(self,text=">", command = lambda: NP.move_relative(3,float(self.M5_Entry_2.get())))
        self.M5_button_3 = ttk.Button(self,text="STOP", command = lambda: NP.stop(3) )
        self.M5_button_4 = ttk.Button(self,text="HOME", command = lambda: NP.move_absolute(3,0) )
        self.M5_button_5 = ttk.Button(self,text="GO", command = lambda: NP.move_absolute(3,float(self.M5_Entry_1.get()))) 

        #MOTOR_No = MOTOR_No-4
        vertical_gap = 0
        
        self.M5_label_1.grid(row = 0+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M5_pos.grid(row=1+vertical_gap,column =1+(MOTOR_No-1)*3)
        self.M5_label_2.grid(row = 2+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M5_Entry_1.grid(row = 3+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M5_label_3.grid(row = 4+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M5_Entry_2.grid(row = 5+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M5_button_1.grid(row = 5+vertical_gap, column =0+(MOTOR_No-1)*3)
        self.M5_button_2.grid(row = 5+vertical_gap, column =2+(MOTOR_No-1)*3)
        self.M5_button_3.grid(row = 6+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M5_button_4.grid(row = 7+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M5_button_5.grid(row = 3+vertical_gap, column =2+(MOTOR_No-1)*3)

        # #-----MOTOR 6------
        MOTOR_No = 6
        self.M6_label_1 = ttk.Label(self,text = "Mask-ROTZ")
        self.M6_label_1.config(font='-weight bold')
        self.M6_pos = ttk.Label(self,text = "0.0")
        
        self.M6_label_2 = ttk.Label(self,text = "Move ABS [deg]")
        self.M6_Entry_1 = ttk.Entry(self)
        
        self.M6_label_3 = ttk.Label(self,text = "Move REL [deg]")
        self.M6_Entry_2 = ttk.Entry(self)

        
        self.M6_button_1 = ttk.Button(self,text="<", command = lambda: KZ.move_relative(3,float('-'+self.M6_Entry_2.get())))
        self.M6_button_2 = ttk.Button(self,text=">", command = lambda: KZ.move_relative(3,float(self.M6_Entry_2.get())))
        self.M6_button_3 = ttk.Button(self,text="STOP", command = lambda: KZ.stop(3) )
        self.M6_button_4 = ttk.Button(self,text="HOME", command = lambda: KZ.home(3) )
        self.M6_button_5 = ttk.Button(self,text="GO", command = lambda: KZ.move_absolute(3,float(self.M6_Entry_1.get())))
        
        
        self.M6_label_1.grid(row = 0+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M6_pos.grid(row=1+vertical_gap,column =1+(MOTOR_No-1)*3)
        self.M6_label_2.grid(row = 2+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M6_Entry_1.grid(row = 3+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M6_label_3.grid(row = 4+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M6_Entry_2.grid(row = 5+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M6_button_1.grid(row = 5+vertical_gap, column =0+(MOTOR_No-1)*3)
        self.M6_button_2.grid(row = 5+vertical_gap, column =2+(MOTOR_No-1)*3)
        self.M6_button_3.grid(row = 6+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M6_button_4.grid(row = 7+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M6_button_5.grid(row = 3+vertical_gap, column =2+(MOTOR_No-1)*3)

        # # #-----MOTOR 7------
        MOTOR_No = 7
        self.M7_label_1 = ttk.Label(self,text = "Sample-X")
        self.M7_label_1.config(font='-weight bold')
        self.M7_pos = ttk.Label(self,text = "0.0")
        
        self.M7_label_2 = ttk.Label(self,text = "Move ABS [mm]")
        self.M7_Entry_1 = ttk.Entry(self)
        
        self.M7_label_3 = ttk.Label(self,text = "Move REL [mm]")
        self.M7_Entry_2 = ttk.Entry(self)
        
        self.M7_button_1 = ttk.Button(self,text="<", command = lambda: NP.move_relative(4,float('-'+self.M7_Entry_2.get())))
        self.M7_button_2 = ttk.Button(self,text=">", command = lambda: NP.move_relative(4,float(self.M7_Entry_2.get())))
        self.M7_button_3 = ttk.Button(self,text="STOP", command = lambda: NP.stop(4) )
        self.M7_button_4 = ttk.Button(self,text="HOME", command = lambda: NP.move_absolute(4,0) )
        self.M7_button_5 = ttk.Button(self,text="GO", command = lambda: NP.move_absolute(4,float(self.M7_Entry_1.get())))
        
        MOTOR_No = MOTOR_No-6
        vertical_gap = 8
        self.M7_label_1.grid(row = 0+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M7_pos.grid(row = 1+vertical_gap,column =1+(MOTOR_No-1)*3)
        self.M7_label_2.grid(row = 2+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M7_Entry_1.grid(row = 3+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M7_label_3.grid(row = 4+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M7_Entry_2.grid(row = 5+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M7_button_1.grid(row = 5+vertical_gap, column =0+(MOTOR_No-1)*3)
        self.M7_button_2.grid(row = 5+vertical_gap, column =2+(MOTOR_No-1)*3)
        self.M7_button_3.grid(row = 6+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M7_button_4.grid(row = 7+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M7_button_5.grid(row = 3+vertical_gap, column =2+(MOTOR_No-1)*3)

        # # #-----MOTOR 8------
        MOTOR_No = 8
        self.M8_label_1 = ttk.Label(self,text = "Sample-Y")
        self.M8_label_1.config(font='-weight bold')
        self.M8_pos = ttk.Label(self,text = "0.0")
        
        self.M8_label_2 = ttk.Label(self,text = "Move ABS [mm]")
        self.M8_Entry_1 = ttk.Entry(self)
        
        self.M8_label_3 = ttk.Label(self,text = "Move REL [mm]")
        self.M8_Entry_2 = ttk.Entry(self)
        
        self.M8_button_1 = ttk.Button(self,text="<", command = lambda: NP.move_relative(5,float('-'+self.M8_Entry_2.get())))
        self.M8_button_2 = ttk.Button(self,text=">", command = lambda: NP.move_relative(5,float(self.M8_Entry_2.get())))
        self.M8_button_3 = ttk.Button(self,text="STOP", command = lambda: NP.stop(5) )
        self.M8_button_4 = ttk.Button(self,text="HOME", command = lambda: NP.move_absolute(5,0) )
        self.M8_button_5 = ttk.Button(self,text="GO", command = lambda: NP.move_absolute(5,float(self.M8_Entry_1.get())))
        
        MOTOR_No = MOTOR_No-6
        vertical_gap = 8
        self.M8_label_1.grid(row = 0+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M8_pos.grid(row = 1+vertical_gap,column =1+(MOTOR_No-1)*3)
        self.M8_label_2.grid(row = 2+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M8_Entry_1.grid(row = 3+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M8_label_3.grid(row = 4+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M8_Entry_2.grid(row = 5+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M8_button_1.grid(row = 5+vertical_gap, column =0+(MOTOR_No-1)*3)
        self.M8_button_2.grid(row = 5+vertical_gap, column =2+(MOTOR_No-1)*3)
        self.M8_button_3.grid(row = 6+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M8_button_4.grid(row = 7+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M8_button_5.grid(row = 3+vertical_gap, column =2+(MOTOR_No-1)*3)

        # # #-----MOTOR 9------
        # MOTOR_No = 9
        # self.M9_label_1 = ttk.Label(self,text = "Sample-Z")
        # self.M9_label_1.config(font='-weight bold')
        # self.M9_pos = ttk.Label(self,text = "0.0")
        
        # self.M9_label_2 = ttk.Label(self,text = "Move ABS [mm]")
        # self.M9_Entry_1 = ttk.Entry(self)
        
        # self.M9_label_3 = ttk.Label(self,text = "Move REL [mm]")
        # self.M9_Entry_2 = ttk.Entry(self)
        
        # self.M9_button_1 = ttk.Button(self,text="<", command = lambda: KZ.move_relative(3,float('-'+self.M9_Entry_2.get())))
        # self.M9_button_2 = ttk.Button(self,text=">", command = lambda: KZ.move_relative(3,float(self.M9_Entry_2.get())))
        # self.M9_button_3 = ttk.Button(self,text="STOP", command = lambda: KZ.stop(3) )
        # self.M9_button_4 = ttk.Button(self,text="HOME", command = lambda: KZ.home(3) )
        # self.M9_button_5 = ttk.Button(self,text="GO", command = lambda: KZ.move_absolute(3,float(self.M9_Entry_1.get())))
        
        # MOTOR_No = MOTOR_No-6
        # vertical_gap = 8
        # self.M9_label_1.grid(row = 0+vertical_gap, column =1+(MOTOR_No-1)*3)
        # self.M9_pos.grid(row = 1+vertical_gap,column =1+(MOTOR_No-1)*3)
        # self.M9_label_2.grid(row = 2+vertical_gap, column =1+(MOTOR_No-1)*3)
        # self.M9_Entry_1.grid(row = 3+vertical_gap, column =1+(MOTOR_No-1)*3)
        # self.M9_label_3.grid(row = 4+vertical_gap, column =1+(MOTOR_No-1)*3)
        # self.M9_Entry_2.grid(row = 5+vertical_gap, column =1+(MOTOR_No-1)*3)
        # self.M9_button_1.grid(row = 5+vertical_gap, column =0+(MOTOR_No-1)*3)
        # self.M9_button_2.grid(row = 5+vertical_gap, column =2+(MOTOR_No-1)*3)
        # self.M9_button_3.grid(row = 6+vertical_gap, column =1+(MOTOR_No-1)*3)
        # self.M9_button_4.grid(row = 7+vertical_gap, column =1+(MOTOR_No-1)*3)
        # self.M9_button_5.grid(row = 3+vertical_gap, column =2+(MOTOR_No-1)*3)

        # # #-----MOTOR 10------
        MOTOR_No = 10
        self.M10_label_1 = ttk.Label(self,text = "Sample-ROTX")
        self.M10_label_1.config(font='-weight bold')
        self.M10_pos = ttk.Label(self,text = "0.0")
        
        self.M10_label_2 = ttk.Label(self,text = "Move ABS [deg]")
        self.M10_Entry_1 = ttk.Entry(self)
        
        self.M10_label_3 = ttk.Label(self,text = "Move REL [deg]")
        self.M10_Entry_2 = ttk.Entry(self)
        
        self.M10_button_1 = ttk.Button(self,text="<", command = lambda: KZ.move_relative(4,float('-'+self.M10_Entry_2.get())))
        self.M10_button_2 = ttk.Button(self,text=">", command = lambda: KZ.move_relative(4,float(self.M10_Entry_2.get())))
        self.M10_button_3 = ttk.Button(self,text="STOP", command = lambda: KZ.stop(4) )
        self.M10_button_4 = ttk.Button(self,text="HOME", command = lambda: KZ.home(4) )
        self.M10_button_5 = ttk.Button(self,text="GO", command = lambda: KZ.move_absolute(4,float(self.M10_Entry_1.get())))
        
        MOTOR_No = MOTOR_No-6
        vertical_gap = 8
        self.M10_label_1.grid(row = 0+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M10_pos.grid(row = 1+vertical_gap,column =1+(MOTOR_No-1)*3)
        self.M10_label_2.grid(row = 2+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M10_Entry_1.grid(row = 3+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M10_label_3.grid(row = 4+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M10_Entry_2.grid(row = 5+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M10_button_1.grid(row = 5+vertical_gap, column =0+(MOTOR_No-1)*3)
        self.M10_button_2.grid(row = 5+vertical_gap, column =2+(MOTOR_No-1)*3)
        self.M10_button_3.grid(row = 6+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M10_button_4.grid(row = 7+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M10_button_5.grid(row = 3+vertical_gap, column =2+(MOTOR_No-1)*3)

        # # #-----MOTOR 11------
        MOTOR_No = 11
        self.M11_label_1 = ttk.Label(self,text = "Sample-ROTY")
        self.M11_label_1.config(font='-weight bold')
        self.M11_pos = ttk.Label(self,text = "0.0")
        
        self.M11_label_2 = ttk.Label(self,text = "Move ABS [deg]")
        self.M11_Entry_1 = ttk.Entry(self)
        
        self.M11_label_3 = ttk.Label(self,text = "Move REL [deg]")
        self.M11_Entry_2 = ttk.Entry(self)
        
        self.M11_button_1 = ttk.Button(self,text="<", command = lambda: NP.move_relative(6,float('-'+self.M11_Entry_2.get())))
        self.M11_button_2 = ttk.Button(self,text=">", command = lambda: NP.move_relative(6,float(self.M11_Entry_2.get())))
        self.M11_button_3 = ttk.Button(self,text="STOP", command = lambda: NP.stop(6) )
        self.M11_button_4 = ttk.Button(self,text="HOME", command = lambda: NP.move_absolute(6,0) )
        self.M11_button_5 = ttk.Button(self,text="GO", command = lambda: NP.move_absolute(6,float(self.M11_Entry_1.get())))
        
        MOTOR_No = MOTOR_No-6
        vertical_gap = 8
        self.M11_label_1.grid(row = 0+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M11_pos.grid(row = 1+vertical_gap,column =1+(MOTOR_No-1)*3)
        self.M11_label_2.grid(row = 2+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M11_Entry_1.grid(row = 3+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M11_label_3.grid(row = 4+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M11_Entry_2.grid(row = 5+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M11_button_1.grid(row = 5+vertical_gap, column =0+(MOTOR_No-1)*3)
        self.M11_button_2.grid(row = 5+vertical_gap, column =2+(MOTOR_No-1)*3)
        self.M11_button_3.grid(row = 6+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M11_button_4.grid(row = 7+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M11_button_5.grid(row = 3+vertical_gap, column =2+(MOTOR_No-1)*3)

        # # #-----MOTOR 12------
        MOTOR_No = 12
        self.M12_label_1 = ttk.Label(self,text = "Sample-ROTZ")
        self.M12_label_1.config(font='-weight bold')
        self.M12_pos = ttk.Label(self,text = "0.0")
        
        self.M12_label_2 = ttk.Label(self,text = "Move ABS [deg]")
        self.M12_Entry_1 = ttk.Entry(self)
        
        self.M12_label_3 = ttk.Label(self,text = "Move REL [deg]")
        self.M12_Entry_2 = ttk.Entry(self)
        
        self.M12_button_1 = ttk.Button(self,text="<", command = lambda: KZ.move_relative(5,float('-'+self.M12_Entry_2.get())))
        self.M12_button_2 = ttk.Button(self,text=">", command = lambda: KZ.move_relative(5,float(self.M12_Entry_2.get())))
        self.M12_button_3 = ttk.Button(self,text="STOP", command = lambda: KZ.stop(5) )
        self.M12_button_4 = ttk.Button(self,text="HOME", command = lambda: KZ.home(5) )
        self.M12_button_5 = ttk.Button(self,text="GO", command = lambda: KZ.move_absolute(5,float(self.M12_Entry_1.get())))
        
        MOTOR_No = MOTOR_No-6
        vertical_gap = 8
        self.M12_label_1.grid(row = 0+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M12_pos.grid(row = 1+vertical_gap,column =1+(MOTOR_No-1)*3)
        self.M12_label_2.grid(row = 2+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M12_Entry_1.grid(row = 3+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M12_label_3.grid(row = 4+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M12_Entry_2.grid(row = 5+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M12_button_1.grid(row = 5+vertical_gap, column =0+(MOTOR_No-1)*3)
        self.M12_button_2.grid(row = 5+vertical_gap, column =2+(MOTOR_No-1)*3)
        self.M12_button_3.grid(row = 6+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M12_button_4.grid(row = 7+vertical_gap, column =1+(MOTOR_No-1)*3)
        self.M12_button_5.grid(row = 3+vertical_gap, column =2+(MOTOR_No-1)*3)


        initialised = 0
        # NP_initialised = 0
        # NPi_initialised = 0
        # KZ_initialised = 0


        for child in self.winfo_children():
            child.grid_configure(padx=6, pady=6)

if __name__ == '__main__':
    root = tkinter.Tk()
    Mo007No2_GUI(root)
    root.mainloop()
