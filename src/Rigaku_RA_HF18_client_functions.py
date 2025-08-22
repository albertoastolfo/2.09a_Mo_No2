# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 10:27:39 2025

@author: Alberto Astolfo
"""

import requests

# this is a simplify version of the functions used for controlling the shutter just to work on the client side
# assuming the PC is on and running the server script

address = "http://128.40.160.162:5000/" 

def get_shutter_state(shutter_no=1):

    response = requests.get("http://128.40.160.162:5000/shutter/status")
    #print(response.json())

    ans = 0
    
    if shutter_no == 1:
        ans = int(response.json()['shutter_1']=='open')
        
    if shutter_no == 2:
        ans = int(response.json()['shutter_2']=='open')
    
    return ans

# Open the specified shutter (1 or 2)
def Open_Shutter(shutter_no):
    # Determine command based on shutter number
    if shutter_no == 1:
        response = requests.post("http://128.40.160.162:5000/shutter/1/open")
    elif shutter_no == 2:
        response = requests.post("http://128.40.160.162:5000/shutter/2/open")
    else:
        raise ValueError("Invalid shutter number. Use 1 or 2.")


# Close the specified shutter (1 or 2)
def Close_Shutter(shutter_no):
    # Determine command based on shutter number
    if shutter_no == 1:
        response = requests.post("http://128.40.160.162:5000/shutter/1/close")
    elif shutter_no == 2:
        response = requests.post("http://128.40.160.162:5000/shutter/2/close")
    else:
        raise ValueError("Invalid shutter number. Use 1 or 2.")

