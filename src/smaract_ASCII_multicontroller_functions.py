# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:20:33 2024

@author: rmapaas
"""

# functions to use Multiple Smaract MSC2 controllers via Ethernet

# make sure you change the IP address of your controllers and update the 'motor2instr' to give back the right controller and axis number



import socket
import binascii
import numpy as np
import struct
from collections import deque

EOF = '\r\n'

def help():
    #print the motor description    
    # print('MOTOR#     Controller#     Description')
    # print('1           0              Sample mask X')
    # print('2           0              Sample mask Z')
    # print('3           0              Sample mask ROTX')
    # print('4           1              Sample mask ROTZ')
    # print('5           1              Sample mask ROTY')
    # print('6           2              Detector mask X')
    # print('7           2              Detector mask Z')
    # print('8           2              Detector mask ROTZ')
    print('MOTOR#     Controller#     Description')
    print('1           0              Dmask X')
    print('2           0              Dmask Z')
    print('3           0              Dmask ROTX')


class Motor_identifier:
    
    # a class to identify the motor axis and controller in one entity
    
    def __init__(self,axis,controller):
        self.axis = str(axis)
        self.controller = int(controller)

def motor2instr(motor):
    
    # it gives both the [motor_ID,instrument_ID] array to move the right axis and controller given the motor number you want to move
    
    
    if motor > 0 and motor < 9:
    
        if motor in [1,2,3]:
            instrument_index = 0
            motor_axis = motor - 1
        else:
            if motor in [4,5]:
                instrument_index = 1
                motor_axis = motor - instrument_index * 3 - 1            
            else:
                if motor in [6,7,8]:
                    instrument_index = 2
                    motor_axis = motor - instrument_index * 3                 

        motor_ID = Motor_identifier(motor_axis,instrument_index)
            
        return motor_ID
            
     
    else:
        help()
        return 0

def check_motor_connection(motor):
    
    # this is to check if the motor controller is available and initialized
    
    Motor_ID = motor2instr(motor)
    
    ans = 0
    
    if Motor_ID != 0:
        try:
            if SM_sockets[Motor_ID.controller] == 'null':
                
                print('Controller not found')
                ans = 0
            else:
                ans = 1
        except:
            print('Not initialized yet.')
            ans = 0
        
    return ans

def check_sockets(number = -1):
    
    # check if the connection is on
    
    ans = 0
    
    if number != -1:
        try:
            SM_sockets[number].send(bytes(':CHAN0:POS?' + EOF,'ascii'))
            ans = 1
        except:
            pass
            #print('OFF')

    else:
        # check all the connections and give 0 is one is closed
        try:
            ans = [0] * len(SM_sockets)
            
            for h in range(len(SM_sockets)):
                ans[h] = check_sockets(h)

        except:
            pass
        # if 0 in ans:
        #     ans = 0
        
    return ans


def init():
    
    global SM_sockets
    
    hosts = ['192.168.1.201','192.168.1.202','192.168.1.200']
    port = 55551    

    #check if the SM_socket is already existing (so init already done before)
    try:
        SM_sockets = SM_sockets
    except:
        SM_sockets = ['null'] * len(hosts)

    for h in range(len(hosts)):
        #if h == 0:
        try:
            # check if it is not connected already
            if not check_sockets(h):        
                tmp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                tmp.settimeout(0.5)
                tmp.connect((hosts[h], port))
                SM_sockets[h] = tmp
        except:
            SM_sockets[h] = 'null'

    return SM_sockets
    
def close():
    
    try:
        for h in SM_sockets:
            try:
                h.close()
                SM_sockets[h] = 'null'
            except:
                pass
    except:
        print('Not initialized yet')
    
    
def get_position(motor):
    # here step is in [mm] if linear and [deg] if rotational
    
    try:
        Motor_ID = motor2instr(motor)
        
        
        cmd = ':CHAN' + str(Motor_ID.axis) +':POS?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[Motor_ID.controller].send(command)
        
        ans = int(read_ans(Motor_ID.controller).rstrip()) * 1e-9
        
        return ans

    except:
        print('Cannot give you the position of channel',str(motor))


def reference(motor):
    
    try:
        Motor_ID = motor2instr(motor)
        
        cmd = ':REF' + str(Motor_ID.axis) + EOF
        
        command = bytes(cmd,'ascii')

        SM_sockets[Motor_ID.controller].send(command)
    except:
        print('Cannot Reference')
    #ans = int(read_ans().rstrip()) * 1e-6
    
    #return ans

def calibration(motor):
    
    try:
        Motor_ID = motor2instr(motor)
        cmd = ':CAL' + str(Motor_ID.axis) + EOF
    
        command = bytes(cmd,'ascii')

        SM_sockets[Motor_ID.controller].send(command)
    except:
        print('Cannot Calibrate')


def stop(motor):
    
    try:
        Motor_ID = motor2instr(motor)
    
        cmd = ':STOP' + str(Motor_ID.axis) + EOF
    
        command = bytes(cmd,'ascii')

        SM_sockets[Motor_ID.controller].send(command)
    except:
        print('Cannot Stop')   
    
    
def move_absolute(motor,target,wait=0):
    
    
    try:
        Motor_ID = motor2instr(motor)
        target_pm = target * 1e9
    
        cmd = ':MOVE' + str(Motor_ID.axis) +' ' + str(target_pm) + EOF
    
        command = bytes(cmd,'ascii')
    
        print(command)
    
        if wait:
            SM_sockets[Motor_ID.controller].send(command)  
            status = 1
            while status == 1:
                #print(status)
                status = isMoving(motor)
        else:
            SM_sockets[Motor_ID.controller].send(command)       

    except:
        print('Cannot Move')

#ans = read_ans().rstrip()

    #print(ans)
    
    
def move_relative(motor,movement,wait=0):
    
    try:
        position = get_position(motor)
        
        move_absolute(motor,position + movement,wait)
    except:
        print('Cannot move')

def get_velocity(motor):
    # here step is in [mm] if linear and [deg] if rotational
    
    try:
        Motor_ID = motor2instr(motor)
        
        cmd = ':CHAN' + str(Motor_ID.axis) +':VEL?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[Motor_ID.controller].send(command)
        
        ans = int(read_ans().rstrip()) * 1e-9
        
        return ans
    except:
        print('Cannot get velocity')
    
 


def set_velocity(motor,new_velocity):
    # here step is in [mm/s] if linear and [deg/s] if rotational
    
    try:
        Motor_ID = motor2instr(motor)
        
        new_vel_pm_s = new_velocity / 1e-9
        
        
        cmd = ':CHAN' + str(Motor_ID.axis) +':VEL ' +str(int(new_vel_pm_s)) + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[Motor_ID.controller].send(command)
    
    except:
        print('Cannot set velocity')
    #ans = int(read_ans().rstrip()) * 1e-6
    
    #return ans     


def get_no_channels(controller):

    try:
        #cmd = ':PROPerty:DEVice:NOCHannels?' + EOF
        cmd = ':DEV:NOCH?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[controller].send(command)
        
        ans = int(read_ans(controller).rstrip())
        
        return ans
    except:
        print('Cannot get the number of channels')


def channel_state(motor):
    
    try:
        Motor_ID = motor2instr(motor)
        
        cmd = ':CHAN' + str(Motor_ID.axis) + ':STAT?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[Motor_ID.controller].send(command)
        
        #ans = int(read_ans().rstrip()) * 1e-6
        
        #ans = np.int32(read_ans(4))
        
        ans = SM_sockets[Motor_ID.controller].recv(4)
        
        #dump = SM_socket.recv(3)
        bits = ''.join(format(byte, '08b') for byte in ans)
        items = deque(bits)
        #items.rotate(37)
        res = ''.join(items)
        print(res)
    
    #clear_buffer()
    
    # not sure it is correct 
    #ans &= 0x00000001
    
        return res
    except:
        pass

def isMoving(motor):
    
    try:
        Motor_ID = motor2instr(motor)
        
        cmd = ':CHAN' + str(Motor_ID.axis) + ':STAT?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[Motor_ID.controller].send(command)
        
        #ans = int(read_ans().rstrip()) * 1e-6
        
        ans = np.int32(read_ans(Motor_ID.controller,4))
           
        clear_buffer()
        
        # not sure it is correct 
        ans &= 0x00000001
        
        return ans

    except:
        pass


def isReferenced(motor):
    
    # note that it does say not referenced only after a power down before a reference procedure
    
    try:
        Motor_ID = motor2instr(motor)
        
        cmd = ':CHAN' + str(Motor_ID.axis) + ':STAT?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[Motor_ID.controller].send(command)
        
        #ans = int(read_ans().rstrip()) * 1e-6
        
        ans = np.int32(read_ans(Motor_ID.controller,4))
        
        #ans = SM_socket.recv(4)
        
        
        clear_buffer()
        
        # this compare the bitmask accordingly with the manual 
        ans &= 0x00000080
        
        if ans == 0x00000080:
            res = 1
        else:
            res = 0
        
        return res    
    
    except:
        pass



def get_hold_time(motor):
    
    try:
        Motor_ID = motor2instr(motor)
        
        cmd = ':CHAN' + str(Motor_ID.axis) + ':HOLD?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[Motor_ID.controller].send(command)
        
        ans = int(read_ans(Motor_ID.controller).rstrip())
    
        
        #ans = read_ans()
        
        return ans   
  
    except:
         pass
  
def clear_buffer(controller):
    
    try:
    
        msg = b''
        last = b'' 
        
        # repeat till a linefeed (10) is received
        try:
            while last != 10:
                print(last)       
                msg = msg + SM_sockets[controller].recv(1)                                    
                #tmp = msg.split(b',')
                last = msg[-1]    
        except:
            print('timeout')

    except:
        pass

    
def No_errors(controller):
    # gives the number of errors in the queue 
    
    try:
        cmd = ':SYST:ERR:COUN?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[controller].send(command)
        
        ans = int(read_ans(controller).rstrip())
        
        return ans
    except:
        pass


def next_error(controller):
    # read the next error in the queue
    
    try:
        cmd = ':SYST:ERR:NEXT?' + EOF
        
        command = bytes(cmd,'ascii')
    
        SM_sockets[controller].send(command)
        
        ans = read_ans(controller).rstrip()
        
        return ans
    
    except:
        pass
    
    
def read_ans(controller,no_bytes = 1):
    
    msg = b''
    last = b'' 
    
    # repeat till a linefeed (10) is received
    while last != 10:
        #print(last)       
        msg = msg + SM_sockets[controller].recv(no_bytes)                                    
        #tmp = msg.split(b',')
        last = msg[-1]

    print(msg)  
    
    return msg

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))