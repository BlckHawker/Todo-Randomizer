import tkinter as tk
import utils
from tkinter import ttk

# todo make it so saved_categories loads from a local json file
# todo make this a dictionary with the key being the name and the value being the Category object
saved_categories_names = ['b', 'c', 'd']
# saved_categories = []

# keeps track of the frames throughout the application
frame_list = []

# the index of the frame that is currently shown to the user
active_frame_index = 0

def make_label(text: str, master, *, side: str | None = None, padx: int | None = None, foreground: str | None = None):
    label = ttk.Label(master = master, text = text, foreground=foreground)
    label.pack(side = side, padx = padx)
    return label

def make_button(text: str, master, side: str | None = None, *, padx: int | None = None, command = None):
    button = ttk.Button(master = master, text = text, command=command)
    button.pack(side = side, padx = padx)
    return button

def organize_saved_categories():
    saved_categories_names.sort()

# changes the active frame on the window
def change_window(frame: tk.Frame):

    print(f'{utils.active_frame_index}')
    # make it so the current frame is disabled
    frame_list[utils.active_frame_index].forget()

    #todo enable to new frame
    frame.pack()

    #todo change the active frame index
    for ix in range(len(frame_list)):
        if(frame_list[ix] == frame):
            utils.active_frame_index = ix
            break






