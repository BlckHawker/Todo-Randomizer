import tkinter as tk
from tkinter import ttk
from functools import partial

from utils import make_label, make_button, saved_categories

# The home page that will show the categories
class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        make_label('Categories', parent)
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

        make_button('Add Category', parent, command=lambda: print('Pressed "Add Category"'))
        self.pack()

    def delete_category(category: str):
        print(f'Deleted category "{category}"')

    def select_category(category: str):
        print(f'Select category "{category}"')
        # When this button is clicked, open a window to show the new category window