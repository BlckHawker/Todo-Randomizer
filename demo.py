import tkinter as tk
from tkinter import ttk
from functools import partial
saved_categories = ['a', 'b', 'c']

def delete_category(category: str):
    print(f'Deleted category "{category}"')

def select_category(category: str):
    print(f'Select category "{category}"')

def make_label(text: str, master, side: str | None = None, padx: int | None = None):
    label = ttk.Label(master = master, text = text)
    label.pack(side = side, padx = padx)
    return label

def make_button(text: str, master, side: str | None = None, *, padx: int | None = None, command = None):
    button = ttk.Button(master = master, text = text, command=command)
    button.pack(side = side, padx = padx)
    return button

#set up window
window = tk.Tk()
window.title('Todo Randomizer')
make_label('Categories', window)


#if there are no categories, make a label to show that
#otherwise, list the categories with their own label
if(not saved_categories):
    make_label('N/A')
else:
    for category in saved_categories:
        category_frame = ttk.Frame(master=window)
        category_frame.pack()
        make_label(category, category_frame, 'left', 10)
        make_button('Select', category_frame, side='left', padx=10, command=partial(select_category, category))
        make_button('Delete', category_frame, side='left', padx=10, command=partial(delete_category, category))

make_button('Add Category', window, command=lambda: print('Pressed "Add Category"'))

#run
window.mainloop()

