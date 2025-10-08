# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 10:27:39 2025

@author: Alberto Astolfo
"""

import requests
import json
import re

# this is a simplify version of the functions used for controlling the shutter just to work on the client side
# assuming the PC is on and running the server script

address = "http://128.40.160.162:5000/" 

def get_shutter_state(shutter_no=1):

    #response = requests.get("http://128.40.160.162:5000/shutter/status")
    response = requests.get("http://128.40.160.162:5000/status", json={"shutter_no": shutter_no})
    #print(response.json())

    data = response.json()

    numbers = re.findall(r'\d+', data['data']['raw'])

    ans = 0
    
    if shutter_no == 1:
        #ans = int(response.json()['shutter_1']=='open')
        ans = int(numbers[3])
        
    if shutter_no == 2:
        #ans = int(response.json()['shutter_2']=='open')
        ans = int(numbers[5])
    
    return ans

def get_state():
    
    response = requests.get("http://128.40.160.162:5000/status")
    
    data = response.json()

    state = re.findall(r'\d+', data['data']['raw'])
    
    return state

def get_kV_from_state(state):
    
    return int(state[0])

def get_mA_from_state(state):
    
    return int(state[1])

def get_shutter1_from_state(state):
    
    return int(state[3])

def get_shutter2_from_state(state):
    
    return int(state[5])


# Open the specified shutter (1 or 2)
def Open_Shutter(shutter_no):
    # Determine command based on shutter number
    if shutter_no == 1 or shutter_no == 2:
        #response = requests.post("http://128.40.160.162:5000/shutter/1/open")
        requests.post("http://128.40.160.162:5000/open", json={"shutter_no": shutter_no})
    else:
        raise ValueError("Invalid shutter number. Use 1 or 2.")


# Close the specified shutter (1 or 2)
def Close_Shutter(shutter_no):
    # Determine command based on shutter number
    if shutter_no == 1 or shutter_no == 2:
        #response = requests.post("http://128.40.160.162:5000/shutter/1/close")
        requests.post("http://128.40.160.162:5000/close", json={"shutter_no": shutter_no})
    else:
        raise ValueError("Invalid shutter number. Use 1 or 2.")

