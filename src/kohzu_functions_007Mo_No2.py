# -*- coding: utf-8 -*-
"""
Created on 12 June 2025

@author: AAstolfo

this is to control the 3 kohzu CRUX-D controllers for the 007Mo setup with single mask

Each CRUX-D control 2 axis and we have 5 motors in total as the following:
    
MOTOR#     Controller#     Description
1           0              Sample mask Z
2           1              Sample mask ROTX
3           1              Sample mask ROTZ
4           2              Sample ROTX
5           2              Sample ROTZ


to avoid confusion with the controllers naming (which is assigned depending which one is ON and seens first)
the offset on motor 1 is used to label the controller with a number between 0 and 4.
This has a minor effect on the homing since the step size is quite small.

"""

import serial
import pyvisa as visa
import numpy as np
import sys
import glob
#import tkinter
#from tkinter import ttk
#from tkinter import filedialog

def help():
    #print the motor description    
    print('MOTOR#     Controller#     Description')
    print('1           0              Sample mask Z')
    print('2           1              Sample mask ROTX')
    print('3           1              Sample mask ROTZ')
    print('4           2              Sample ROTX')
    print('5           2              Sample ROTZ')


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def init(connection_type_input = 1):
    
    # initialization of the controllers it can find.
    # With standard configuration it is 9 motors Kohzu over 5 controllers

    global prefix_cmd,instr_ordered,connection_type
    
    connection_type = connection_type_input # 0 for VISA; 1 for SERIAL
    
    
    # this will keep 'null' if the right controller is not found
    instr_ordered = ['null','null','null']
    
    
    if connection_type == 0:
    
        # in case of connection via USB (in this case it needs the '\02' on the command)
        prefix_cmd = '\x02'
        
        # search for resources via pyvisa
        rm = visa.ResourceManager()
        #print(rm.list_resources())
        resources = rm.list_resources()
        
        # find the CRUX-D controllers available
        for i in resources[1:]:
            
            print(i)
            
            try:
                # sending the identification command to find the CRUX-D units
                instr = rm.open_resource(i)
                command = prefix_cmd +'IDN'
                ans = instr.query(command).split('\t')
                
                if ans[2] == 'CRUX-D':
                    print('Controller: ',ans[2])
                    
                    # look at the label OFFSET (see above comment)
                    ans = -int(instr.query(prefix_cmd + 'RSY1/1').split('\t')[-1])
                    print('Controller ID: ',ans,'\n')
                    instr_ordered[-ans] = instr
            
            except:
                pass
    
    if connection_type == 1:
        prefix_cmd = ''
    
        resources = serial_ports()

        # find the CRUX-D controllers available
        for i in resources:
            
            print(i)
            
            try:
                # sending the identification command to find the CRUX-D units
                ser = serial.Serial(port = i, baudrate = 9600, bytesize = 8, timeout = 2)                 
                cmd = 'IDN'
                command = [2]+[ord(c) for c in cmd]+[13,10] 
                ser.write(command)
                
                ans = str(ser.readline()).split('\\t')
                
                if ans[2] == 'CRUX-D':
                    print('Controller: ',ans[2])
                    
                    # look at the label OFFSET (see above comment)
                    cmd = 'RSY1/1'
                    command = [2]+[ord(c) for c in cmd]+[13,10]
                    ser.write(command)
                    ans = -int(str(ser.readline()).split('\\t')[-1].replace("\\r\\n'",""))
                    print('Controller ID: ',ans,'\n')
                    instr_ordered[ans] = ser
            
            except:
                pass             
    
    print(instr_ordered)
    

class Motor_identifier:
    
    # a class to identify the motor axis and controller in one entity
    
    def __init__(self,axis,controller):
        self.axis = str(axis)
        self.controller = int(controller)

def motor2instr(motor):
    
    # it gives both the [motor_ID,instrument_ID] array to move the right axis and controller given the motor number you want to move
    
    if motor > 0 and motor < 6:

        if motor == 1:
            instrument_index = 0
        
            motor_axis = 1
        
        if motor == 2:
            instrument_index = 1
        
            motor_axis = 1        
        
        if motor == 3:
            instrument_index = 1
        
            motor_axis = 2
            
        if motor == 4:
            instrument_index = 2
        
            motor_axis = 1

        if motor == 5:
            instrument_index = 2
        
            motor_axis = 2            
              
        motor_ID = Motor_identifier(motor_axis,instrument_index)
    
        return motor_ID
    else:
        help()
        return 0

def check_motor_connection(motor):
    
    # this is to check if the motor controller is available and initialized
    
    Motor_ID = motor2instr(motor)
    
    try:
        if instr_ordered[Motor_ID.controller] == 'null':
            
            print('Controller not found')
            ans = 0
        else:
            ans = 1
    except:
        print('Not initialized yet.')
        ans = 0
    
    return ans
    

def step2unit(motor):
    
    # conversion for converting the unit into steps and viceversa
    
    if motor > 0 and motor < 10:
    
        #k1 = 0.000084    # step size for SA10A-RM at 1/20 microstep division [motor1]
        #k2 = 0.00011    # step size for SA10A-RT at 1/20 microstep division [motor2]
        #k1 = 0.00048    # step size for SA07A-R2M at 1/20 microstep division [motor1]
        #k2 = 0.00048    # step size for SA07A-R2T at 1/20 microstep division [motor2] 
        #k1 = 0.0000206    # step size for SA10A-R2L01 (R2M01) at 1/20 step division [motor1]
        #k2 = 0.00001615   # step size for SA10A-R2L01 (R2B01)   at 1/20 step division [motor2]
        k1 = 0.001      #       SXA530-R01
        k2 = 0.001062   #       SA05A-R2G01
        k3 = 0.001      #       SXA530-R01
        k4 = 1#0.0005     #       ZA04A-W101
        k5 = 1#0.00099    #       SA04B-RS02 (1)
        # k6 = 0.00134    #       SA04B-RS02 (2)
        # k7 = 0.001      #       SYA0530-R01 (1)
        # k8 = 0.001      #       SYA0530-R01(2)
        # k9 = 0.001062   #       SA05A-R2G01
             
        
        constant = k1 * int(motor == 1) + k2 * int(motor == 2) + k3 * int(motor == 3) + k4 * int(motor == 4) + k5 * int(motor == 5)# + k6 * int(motor == 6) + k7 * int(motor == 7) + k8 * int(motor == 8) + k9 * int(motor == 9)
        
        resolution = microstep_set(motor)
        
        step_value = constant / resolution
        
        return step_value

    else:
        help()
        return 0
    
def unit_name(motor):
    
    # to have the unit specific for the motor (simply hardcoded)
    
    motor = int(motor)
    
    if motor > 0 and motor < 6:
    
        if motor in [1]:
            unit = 'mm'
        else:
            unit = 'deg'

        return unit

    else:
        help()
        return 0    


def microstep_set(motor):
    
    # read the setting on the controller to get the microstep setting and calculate the conversion factors for the movements
    
    if motor > 0 and motor < 6:
    
        Motor_ID = motor2instr(motor)
        
        motor = Motor_ID.axis
    
        msg = sendcmd('RSY'+str(motor)+'/66',Motor_ID.controller)
        #print(msg)
        
        if connection_type == 0:
            Setting_No = int(msg.split('\t')[3])
        else:
            Setting_No = int(msg.split('\\t')[3].replace("\\r\\n'",""))
        #print(Setting_No)
        
        # table taken from the manual
        conversion_table = [1,2,2.5,4,5,8,10,20,25,40,50,80,100,125,200,250]
        
        resolution = conversion_table[Setting_No-1]
        
        return resolution

    else:
        help()
        return 0


def close():

    # close the connection(s)
    if connection_type == 0:
        for i in instr_ordered:   
            if i != 'null':
                print(i)
                i.close()
    
    if connection_type == 1:
    
        for i in instr_ordered:
            if i != 'null':
                print('closing:',i)
                i.close()
            
    
    
def sendcmd(cmd,controller_index):
    
    # send the command to the controller [0,4]
    # cmd is a string as 'IDN' for example
    
    if connection_type == 0:
        try:
                command = prefix_cmd + cmd
                
                instr = instr_ordered[controller_index]
                
                msg = instr.query(command)
            
                return msg
        except:
            pass
    
    if connection_type == 1:
        try:
                command = [2]+[ord(c) for c in cmd]+[13,10]
                
                ser = instr_ordered[controller_index]
                ser.write(command)
                msg = str(ser.readline())

            
                return msg
        except:
            pass    
    
    
    
def get_position(motor,no_print = 0):
    
    # get the motor position as a number and prints it with the appropriate units
    
    
    if motor > 0 and motor < 10:
    
        Motor_ID = motor2instr(motor)
        constant = step2unit(motor)
        unit = unit_name(motor)
        
        # rename the motor since the controller accepts only 1 or 2 
        motor = Motor_ID.axis
        
        try:
            msg = sendcmd('RDP'+str(motor),Motor_ID.controller)
            #print(msg)
            if connection_type == 0:
                tmp = msg.split('\t')
            else:
                tmp = msg.split('\\t')
            #constant = step2unit(motor)
            position = int(float(tmp[len(tmp)-1].replace("\\r\\n'",""))) * constant
            
            if no_print == 0:
                print(position, unit)
            
            return position
        except:
            pass

    else:
        help()
        return 0      


def move_relative(motor,movement,wait = 0):

    # move relative the motor

    if motor > 0 and motor < 10:
    
        Motor_ID = motor2instr(motor)
        constant = step2unit(motor)
         
        motor = Motor_ID.axis    
        
        if type(movement) == str:
            try:
                mov = float(movement)
            except (ValueError, TypeError):
                print('Type a number')
            else:
                steps = round(mov / constant)
        else:
            steps = round(movement / constant)
        
    
        msg = sendcmd('RPS'+str(motor)+'/9/'+str(steps)+'/1',Motor_ID.controller)
        
        if wait != 0:
            
            status = statusRead(motor)
            while status == 1:
                status = statusRead(motor)
                #print('wait to arrive...')
        
        
        return msg

    else:
        help()
        return 0 


def move_absolute(motor,target,wait = 0):

    
    if motor > 0 and motor < 10:
        Motor_ID = motor2instr(motor)
        constant = step2unit(motor)
         
        motor = Motor_ID.axis  
    
        if type(target) == str:
            try:
                tar = float(target)
            except (ValueError, TypeError):
                print('Type a number')
            else:
                steps = round(tar / constant)
        else:    
            steps = round(target / constant)
        
    
        msg = sendcmd('APS'+str(motor)+'/9/'+str(steps)+'/1',Motor_ID.controller)

        if wait != 0:
            
            status = statusRead(motor)
            while status == 1:
                status = statusRead(motor)
                #print('wait to arrive...')

    
        return msg

    else:
        help()
        return 0 


def get_origin_offset(motor):
    # read the offset set for the origin
    # NB: this is used to label the controllers
    
    msg = sendcmd('RSY'+str(motor)+'/1')
    
    #print(msg)
    
    if connection_type == 0:
        offset = int(msg.split('\t')[-1])
    else:
        offset = int(msg.split('\\t')[-1].replace("\\r\\n'",""))
    
    return offset    
    
def statusRead(motor):
    # get the status of the motor. 0 for still, 1 for moving

    motor = int(motor)

    if motor > 0 and motor < 6:
        Motor_ID = motor2instr(motor)
        motor = Motor_ID.axis  

    #msg = sendcmd('STR'+str(motor))
    msg = sendcmd('STR'+str(motor),Motor_ID.controller)
    
    
    status = int(msg.split('\\t')[2])
 
    return status    

def stop(motor):
    
    Motor_ID = motor2instr(motor)
    
    motor = Motor_ID.axis 
    
    msg = sendcmd('STP'+str(motor)+'/0',Motor_ID.controller)
    return msg

def cleanans(ans):
    msg = ans.decode('ascii')
    return msg
    
def home(motor):

    if motor > 0 and motor < 6:    

        Motor_ID = motor2instr(motor)
        
        motor = Motor_ID.axis    
    
    
        msg = sendcmd('ORG'+str(motor)+'/9/1',Motor_ID.controller)
        #msg = kohzu_sendcmd('ORG'+str(motor)+'/1/0/1/3/0')

    
        return msg
    
    else:
        help()
        return 0 
