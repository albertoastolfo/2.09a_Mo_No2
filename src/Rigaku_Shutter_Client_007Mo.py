# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 10:19:14 2025

@author: rmapaas
"""

import tkinter as tk
import Rigaku_RA_HF18_client_functions as shutter

# Define initial status for each shutter: 'open' or 'closed'

#msg = shutter.check_status()
status_shutter_1 = shutter.get_shutter_state(1)
status_shutter_2 = shutter.get_shutter_state(2)

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

root = tk.Tk()
root.title("AXIm - Shutter Control")
root.geometry("400x300")
root.configure(bg="#f7f9fc")

# Title
title = tk.Label(root, text="AXIm - Shutter Control", font=("Verdana", 18, "bold"), bg="#f7f9fc", fg="#34495e")
title.pack(pady=10)

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

    # Determine initial label text and color
    status = initial_status.get(shutter_num, 'closed')
    if shutter_num == 1:
        label_text = f"Shutter {shutter_num}: Disabled"
        label_color = "#7f8c8d"  # Gray
    else:
        label_text = f"Shutter {shutter_num}: {'Open' if status == 'open' else 'Closed'}"
        label_color = "#e74c3c" if status == 'open' else "#2ecc71"

    label = tk.Label(frame, text=label_text, font=("Verdana", 12), fg=label_color, bg="#ecf0f1")
    label.pack(pady=5)

    btn_frame = tk.Frame(frame, bg="#ecf0f1")
    btn_frame.pack()

    if shutter_num == 2:
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

root.mainloop()