import tkinter as tk
from tkinter import ttk

def make_label(text: str, master, side: str | None = None, padx: int | None = None):
    label = ttk.Label(master = master, text = text)
    label.pack(side = side, padx = padx)
    return label

def make_button(text: str, master, side: str | None = None, *, padx: int | None = None, command = None):
    button = ttk.Button(master = master, text = text, command=command)
    button.pack(side = side, padx = padx)
    return button

# todo make it so saved_categories loads from a local json file
saved_categories = ['a', 'b', 'c']
# saved_categories = []
