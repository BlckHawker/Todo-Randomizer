import tkinter as tk
import utils
from Task import Task
from Category import Category
from functools import partial

from tkinter import ttk

# todo make it so saved_categories loads from a local json file
# todo make this a dictionary with the key being the name and the value being the Category object
saved_categories = {
    'a': Category('a'),
    'b': Category('b'),
    'c': Category('c'),

}

# keeps track of the frames throughout the application
frame_list = []

# the index of the frame that is currently shown to the user
active_frame_index = 0

def make_label(text: str, master, *, side: str | None = None, padx: int | None = None, foreground: str | None = None):
    label = ttk.Label(master = master, text = text, foreground=foreground)
    label.pack(side = side, padx = padx)
    return label

def make_button(text: str, master, *, side: str | None = None, padx: int | None = None, command = None):
    button = ttk.Button(master = master, text = text, command=command)
    button.pack(side = side, padx = padx)
    return button

def organize_saved_categories():
    utils.saved_categories = dict(sorted(utils.saved_categories.items()))

# changes the active frame on the window
def change_window(frame: tk.Frame):

    # make it so the current frame is disabled
    frame_list[utils.active_frame_index].forget()

    #enable to new frame
    frame.pack()

    #change the active frame index
    for ix in range(len(frame_list)):
        if(frame_list[ix] == frame):
            utils.active_frame_index = ix
            break


# Helper function that creates a pop up window
# that accepts one text input
def create_pop_up_with_input(master, label_text, button_method):
    top= tk.Toplevel(master=master)
    input_frame = ttk.Frame(top)
    input_frame.pack()
    utils.make_label(text=label_text, master=input_frame, side= 'left')
    entryStr = tk.StringVar()
    entry = ttk.Entry(input_frame, textvariable=entryStr)
    entry.pack()
    button_frame = ttk.Frame(top)
    button_frame.pack()
    # make a warning text that will pop up when the user inputs an invalid thing
    warning_label = utils.make_label(text="Warning label", master=top, foreground="red")
    warning_label.forget()
    utils.make_button(text="Cancel", master=button_frame, side= 'left', command=lambda: top.destroy()) # When the cancel button is clicked, close this window
    utils.make_button(text= "Submit", master=button_frame, side= 'left', command=partial(button_method, entryStr, warning_label))
    
    top.transient(master=master) # set to be on top of the main window
    top.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
    master.wait_window(master) # pause anything on the main window until this one closes
    pass
