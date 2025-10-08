# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 10:19:14 2025

@author: rmapaas
"""

import tkinter as tk
import Rigaku_shutter_client_functions as shutter
import requests

# Define initial status for each shutter: 'open' or 'closed'

#msg = shutter.check_status()
#status_shutter_1 = shutter.get_shutter_state(1)
#status_shutter_2 = shutter.get_shutter_state(2)

status = shutter.get_state()
status_shutter_1 = shutter.get_shutter1_from_state(status)
status_shutter_2 = shutter.get_shutter2_from_state(status)
#print(status_shutter_1)
#print(status_shutter_2)

shutter_wanted = 2

initial_status = {
    1: 'open' if status_shutter_1 else 'closed',
    2: 'open' if status_shutter_2 else 'closed'
}

def open_shutter(label, shutter_num):
    shutter.Open_Shutter(shutter_num)
    
    # check if the shutter is really open
    status = shutter.get_shutter_state(shutter_num)
    
    if status:
        label.config(text=f"Shutter {shutter_num}: Open", fg="#e74c3c")  # Red
        #print('open', shutter_num)

def close_shutter(label, shutter_num):
    
    shutter.Close_Shutter(shutter_num)
    
    # check if the shutter is really closed
    status = shutter.get_shutter_state(shutter_num)
    
    if not status:
        label.config(text=f"Shutter {shutter_num}: Closed", fg="#2ecc71")  # Green 
        #print('close', shutter_num)

def update_shutter_status(label, shutter_num):
    status = shutter.get_shutter_state(shutter_num)
    #print("Status object:", status)
    
    
    if shutter_num == 2:
        label.config(text=f"Shutter {shutter_num}: Disabled", fg="#7f8c8d")
    else:
        label_text = f"Shutter {shutter_num}: {'Open' if status else 'Closed'}"
        label_color = "#e74c3c" if status else "#2ecc71"
        label.config(text=label_text, fg=label_color)
    
    # Schedule next update in 5 seconds
    #root.after(10000, update_shutter_status, label, shutter_num)
    #root.after(5000, lambda: update_entries(label, shutter_num))
    root.after(5000, update_entries, label, shutter_num)

def update_entries(label, shutter_num):
    
    try:
        status = shutter.get_state()
        #print("DEBUG: status =", status) 
        if shutter_num != shutter_wanted:
            label.config(text=f"Shutter {shutter_num}: Disabled", fg="#7f8c8d")
        else:
            sh1 = shutter.get_shutter1_from_state(status)
            #print('sh1 = ',sh1 )
            label_text = f"Shutter {shutter_num}: {'Open' if sh1 else 'Closed'}"
            label_color = "#e74c3c" if sh1 else "#2ecc71"
            label.config(text=label_text, fg=label_color)        
        
        
        
        
        kv = shutter.get_kV_from_state(status)
        #print(kv)
        ma = shutter.get_mA_from_state(status)
        #print(ma)
        kv_label.config(text=f"kV: {kv}")
        ma_label.config(text=f"mA: {ma}")
        #print('here')
        
    except Exception as e:
        kv_label.config(text="kV: Error")
        ma_label.config(text="mA: Error")
        #print("Status fetch failed:", e)

    root.after(10000, lambda: update_entries(label, shutter_num))

# def update_entries(label, shutter_num):
#     try:
#         status = shutter.get_state()
#         print("DEBUG: status =", status)  # This will show you what you're working with
        

# def update_entries(label, shutter_num):
#     kv_label.config(text="kV: 20")
#     ma_label.config(text="mA: 10")
#     label.config(text=f"Shutter {shutter_num}: Open", fg="#e74c3c")
#     root.after(5000, lambda: update_entries(label, shutter_num))


# def update_kv_ma():
#     try:
#         response = requests.get("http://localhost:5000/status")  # Adjust URL if needed
#         data = response.json()
#         if data['status'] == 'success':
#             kv = data['data']['kV']
#             ma = data['data']['mA']
#             kv_label.config(text=f"kV: {kv}")
#             ma_label.config(text=f"mA: {ma}")
#     except Exception as e:
#         kv_label.config(text="kV: Error")
#         ma_label.config(text="mA: Error")
#         print("Status fetch failed:", e)

#     # Schedule next update in 5 seconds
#     root.after(5000, update_kv_ma)

root = tk.Tk()
root.title("AXIm - Shutter Control")
root.geometry("")
#root.geometry("400x300")
root.configure(bg="#f7f9fc")

# Title
title = tk.Label(root, text="AXIm - Shutter Control", font=("Verdana", 18, "bold"), bg="#f7f9fc", fg="#34495e")
title.pack(pady=10)

kv_label = tk.Label(root, text="kV: --", font=("Verdana", 12), bg="#f7f9fc", fg="#34495e")
kv_label.pack(pady=5)

ma_label = tk.Label(root, text="mA: --", font=("Verdana", 12), bg="#f7f9fc", fg="#34495e")
ma_label.pack(pady=5)


# Button styling function
def style_button(btn, bg, hover_bg):
    btn.configure(bg=bg, fg="white", activebackground=hover_bg, font=("Verdana", 10), width=12, relief="flat")
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))

# THIS IS TO CONTROL BOTH SHUTTERS

# Create shutter control frame with initial status
# def create_shutter_frame(shutter_num):
#     frame = tk.Frame(root, bg="#ecf0f1", bd=2, relief="groove")
#     frame.pack(padx=20, pady=10, fill="x")

#     # Determine initial label text and color
#     status = initial_status.get(shutter_num, 'closed')
#     if status == 'open':
#         label_text = f"Shutter {shutter_num}: Open"
#         label_color = "#e74c3c"  # Red
#     else:
#         label_text = f"Shutter {shutter_num}: Closed"
#         label_color = "#2ecc71"  # Green

#     label = tk.Label(frame, text=label_text, font=("Verdana", 12), fg=label_color, bg="#ecf0f1")
#     label.pack(pady=5)

#     btn_frame = tk.Frame(frame, bg="#ecf0f1")
#     btn_frame.pack()

#     open_btn = tk.Button(btn_frame, text="Open", command=lambda: open_shutter(label, shutter_num))
#     close_btn = tk.Button(btn_frame, text="Close", command=lambda: close_shutter(label, shutter_num))

#     style_button(open_btn, "#e74c3c", "#c0392b")  # Red for open
#     style_button(close_btn, "#2ecc71", "#27ae60")  # Green for close

#     open_btn.pack(side="left", padx=5, pady=5)
#     close_btn.pack(side="left", padx=5, pady=5)


# THIS IS TO DISABLE ONE OR THE OTHER SHUTTER

def create_shutter_frame(shutter_num):
    frame = tk.Frame(root, bg="#ecf0f1", bd=2, relief="groove")
    frame.pack(padx=20, pady=10, fill="x")
    
    #shutter_wanted = 1
    
    # Determine initial label text and color
    status = initial_status.get(shutter_num, 'closed')
    if shutter_num != shutter_wanted:
        label_text = f"Shutter {shutter_num}: Disabled"
        label_color = "#7f8c8d"  # Gray
    else:
        label_text = f"Shutter {shutter_num}: {'Open' if status == 'open' else 'Closed'}"
        label_color = "#e74c3c" if status == 'open' else "#2ecc71"

    label = tk.Label(frame, text=label_text, font=("Verdana", 12), fg=label_color, bg="#ecf0f1")
    label.pack(pady=5)

    # Start regular updates
    #update_shutter_status(label, shutter_num)
    
    # so we update the entries only one time at the beginning
    if shutter_num == shutter_wanted:
        update_entries(label,shutter_num)

    btn_frame = tk.Frame(frame, bg="#ecf0f1")
    btn_frame.pack()

    if shutter_num == shutter_wanted:
        open_btn = tk.Button(btn_frame, text="Open", command=lambda: open_shutter(label, shutter_num))
        close_btn = tk.Button(btn_frame, text="Close", command=lambda: close_shutter(label, shutter_num))

        style_button(open_btn, "#e74c3c", "#c0392b")
        style_button(close_btn, "#2ecc71", "#27ae60")

        open_btn.pack(side="left", padx=5, pady=5)
        close_btn.pack(side="left", padx=5, pady=5)
    else:
        disabled_label = tk.Label(btn_frame, text="Controls Disabled", font=("Verdana", 10, "italic"), fg="#7f8c8d", bg="#ecf0f1")
        disabled_label.pack(pady=5)


# Create both shutter frames
create_shutter_frame(1)
create_shutter_frame(2)

#update_entries()
root.mainloop()