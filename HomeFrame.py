import tkinter as tk
from tkinter import ttk
from functools import partial

from utils import make_label, make_button, saved_categories

# The home page that will show the categories
class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        make_label('Categories', parent)
        self.parent = parent
        #if there are no categories, make a label to show that
        #otherwise, list the categories with their own label
        if(len(saved_categories) == 0):
            category_frame = ttk.Frame(master=parent)
            category_frame.pack()
            make_label('N/A', category_frame, 'left', 10)
        else:
            for category in saved_categories:
                category_frame = ttk.Frame(master=parent)
                category_frame.pack()
                make_label(category, category_frame, 'left', 10)
                make_button('Select', category_frame, side='left', padx=10, command=partial(self.select_category, category))
                make_button('Delete', category_frame, side='left', padx=10, command=partial(self.delete_category, category))

        make_button('Add Category', parent, command=self.add_category_button_press)
        self.pack()

    def delete_category(category: str):
        print(f'Deleted category "{category}"')

    def select_category(category: str):
        print(f'Select category "{category}"')
        # When this button is clicked, open a window to show the new category window

    def add_category_button_press(self):
        top= tk.Toplevel(self.parent)
        input_frame = ttk.Frame(top)
        input_frame.pack()
        make_label(text= "Choose the name of the new category:", master=input_frame, side= 'left')
        entryStr = tk.StringVar()
        entry = ttk.Entry(input_frame, textvariable=entryStr)
        entry.pack()
        button_frame = ttk.Frame(top)
        button_frame.pack()
        make_button(text="Cancel", master=button_frame, side= 'left', command=lambda: top.destroy()) # When the cancel button is clicked, close this window
        make_button(text= "Submit", master=button_frame, side= 'left', command=partial(self.submit_category_check, entryStr))
        top.transient(self.parent) # set to be on top of the main window
        top.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
        self.parent.wait_window(self) # pause anything on the main window until this one closes

    def submit_category_check(self, entryStr):

        # get the trimmed input
        input = entryStr.get().strip()
        print('input: ' + input)

        # input can't be empty
        if(input == ""):
            print("input is empty")
            pass
        # input can't already be in saved_categories
        for category in saved_categories:
            if(category.upper() == input.upper()):
                print("input has already been found in the list")
                pass
        