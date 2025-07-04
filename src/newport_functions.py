# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 13:13:09 2018

@author: AAstolfo
"""

import socket
import numpy as np

def init():
    
    # initialize the Newport controller
    # make sure the IP is correct
    
    global NP_sockets
    
    No_motors = 8
    
    # it creates a socket per motor plus two extra for stop and position reading
    No_sockets = No_motors + 2

    #host = '192.168.5.254'
    host = '192.168.254.254'
    port = 5001    
    
    for i in range(0,No_sockets):
        if i == 0:
            tmp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tmp.settimeout(0.5)
            tmp.connect((host, port))
            NP_sockets = [tmp] * No_sockets
        else:
            tmp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tmp.connect((host, port))
            NP_sockets[i] = tmp
    
    # add this part to initialize the speed for the translator which is quite high as default
    tmp = set_velocity(1,30,250)
    # add this part to initialize the speed for the rotator which is quite high as default
    tmp = set_velocity(2,72,100)
    
    
    return NP_sockets

def sendcmd(cmd,socket,read_answer):
    
    # send a command to the controller
    # if read_answer = 0 if does NOT read the answer
    # if read_answer = 1 if does read the answer
    
    command = bytes(cmd,'ascii')
    
    NP_sockets[socket].send(command)
    
    if read_answer == 1:
        ans = readans(socket)
    else:
        ans = ''
    
    return ans
        

def readans(socket):
    # read the answer from the controller
    
    msg = b''
    last = b'' 
    
    while last != b'EndOfAPI':
        #print(last+b'merda')        
        msg = msg + NP_sockets[socket].recv(1)                                    
        tmp = msg.split(b',')
        last = tmp[len(tmp)-1]
    
    #print(msg)    
    return msg

def get_position(motor):
    # it get the position of the motor
    # it prints an error if motor does not exist for example
    
    try:    
        cmd = 'GroupPositionCurrentGet(Group'+str(motor)+',double  *)'
        pos_socket = len(NP_sockets) -1
        ans = sendcmd(cmd,pos_socket,1)
        tmp = ans.split(b',')
        #print(tmp)
        pos = float(tmp[1])
        #print(pos)
        return pos
    except:
        print('Error')

def move_relative(motor, step, wait=0):
    # move relatively the motor
    # set wait=1 to return after the motion completed
    
    try:
        cmd = 'GroupMoveRelative(Group'+str(motor)+','+str(step)+')'
        if wait ==1:
            sendcmd(cmd,motor,1)  
            status = 1
            while status == 1:
                #print(status)
                status = get_motion_status(motor)
        else:
            sendcmd(cmd,motor,0)
    except:
        print('Error')
    
def move_absolute(motor, target, wait=0):
    # move absolutely the motor
    # set wait=1 to return after the motion completed
    
    try:
        cmd = 'GroupMoveAbsolute(Group'+str(motor)+','+str(target)+')'
        if wait == 1:
            sendcmd(cmd,motor,1)  
            status = 1
            while status == 1:
                #print(status)
                status = get_motion_status(motor)
        else:
            sendcmd(cmd,motor,0)
    except:
       print('Error') 
    
    
def stop(motor):
    # stop the motion of a specific motor
    
    try:
        cmd = 'GroupMoveAbort(Group'+str(motor)+')'
        sendcmd(cmd,0,1) 
    except:
        print('Error') 

def get_velocity(motor):
    # get the set velocity of a motor
    
    try:
        cmd = 'PositionerSGammaParametersGet(Group'+str(motor)+'.Pos,double *,double *,double *,double *)'
        
        pos_socket = len(NP_sockets) -1
        ans = sendcmd(cmd,pos_socket,1) 
        #ans = NP_sendcmd(cmd,motor,1)     
        #print(ans)
        tmp = ans.split(b',')
        values = [float(tmp[0]),float(tmp[1]),float(tmp[2]),float(tmp[3]),float(tmp[4])]
        #print(float(tmp[1]))
        return values
    except:
        print('Error') 

def get_current_velocity(motor):
    # Get current velocity of the motor
    
    try:
        cmd = 'GroupVelocityCurrentGet(Group'+str(motor)+',double *)'
        pos_socket = len(NP_sockets) -1
        ans = sendcmd(cmd,pos_socket,1)     
        tmp = ans.split(b',')
        values = float(tmp[1])
        #print(float(tmp[1]))
        return values
    except:
        print('Error') 

def get_motion_status(motor):
    #Get motion status
    
    try:
        pos_socket = len(NP_sockets) -1
        cmd = 'GroupMotionStatusGet(Group'+str(motor)+',int *)'
        ans = sendcmd(cmd,pos_socket,1)
        #print(ans)
        tmp = ans.split(b',')
        values = int(tmp[1])
        return values
    except:
        print('Error') 
    
def get_status(motor):
    #Get motion status
    
    try:
        pos_socket = len(NP_sockets) -1
        cmd = 'GroupStatusGet(Group'+str(motor)+',int *)'
        ans = sendcmd(cmd,pos_socket,1)
        tmp = ans.split(b',')
        values = int(tmp[1])
        return values
    except:
        print('Error') 
        return 0

def set_velocity(motor,velocity,acceleration):
    # Set the velocity and acceleration of a specific motor
    
    
    try:
        old_velocity =get_velocity(motor) 
        #cmd = 'PositionerSGammaParametersSet(Group'+str(motor)+'.Pos,'+str(velocity)+','+str(old_velocity[2])+','+str(old_velocity[3])+','+str(old_velocity[4])+')'
        cmd = 'PositionerSGammaParametersSet(Group'+str(motor)+'.Pos,'+str(velocity)+','+str(acceleration)+','+str(old_velocity[3])+','+str(old_velocity[4])+')'
        
        pos_socket = len(NP_sockets) -1
        ans = sendcmd(cmd,pos_socket,1)
        #ans = NP_sendcmd(cmd,motor,1)
        #tmp = ans.split(b',')
        #print(ans)
        #print(float(tmp[1])) 
        return ans
    except:
        print('Error') 

def initialize(motor):
    
    # initialize a motor
    
    try:
        cmd = 'GroupInitialize(Group'+str(motor)+')'
        sendcmd(cmd,0,1)
    except:
        print('Error') 

def home(motor):
    
    # home a motor
    
    try:
        cmd = 'GroupHomeSearch(Group'+str(motor)+')'
        sendcmd(cmd,0,1)
    except:
        print('Error') 

def get_position_all():
    
        No_Motors = len(NP_sockets) - 2
        
        All_positions = np.zeros(No_Motors)
        
        for i in range(1,No_Motors+1):
            try:
                position = get_position(i)
                All_positions[i-1] = position
                print(" Motor #" + str(i) + ' = ' + str(position))
            except:
                pass
        return All_positions

def initialize_and_home(motor):
    # this is to run the initialization and homing in sequence waiting it to finish it
    try:
        status = get_status(motor)
        if status < 10:
            initialize(motor)
            home(motor) 
    except:
        print('Error') 

def close():
    # close all the sockets
    
    for i in NP_sockets:
        i.close()