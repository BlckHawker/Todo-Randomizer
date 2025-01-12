import tkinter as tk
from tkinter import ttk
from functools import partial

# todo make it so saved_categories loads from a local json file
# saved_categories = ['a', 'b', 'c']
saved_categories = []

def delete_category(category: str):
    print(f'Deleted category "{category}"')

def select_category(category: str):
    print(f'Select category "{category}"')
    # When this button is clicked, open a window to show the new category window

def make_label(text: str, master, side: str | None = None, padx: int | None = None):
    label = ttk.Label(master = master, text = text)
    label.pack(side = side, padx = padx)
    return label

def make_button(text: str, master, side: str | None = None, *, padx: int | None = None, command = None):
    button = ttk.Button(master = master, text = text, command=command)
    button.pack(side = side, padx = padx)
    return button


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
                make_button('Select', category_frame, side='left', padx=10, command=partial(select_category, category))
                make_button('Delete', category_frame, side='left', padx=10, command=partial(delete_category, category))

        make_button('Add Category', parent, command=lambda: print('Pressed "Add Category"'))
        self.pack()


# The window created to show a GUI to a use
class Window():
    def __init__(self, master):
        mainframe = tk.Frame(master)
        mainframe.pack()

        # the index of the frame that is currently shown to the user
        self.activeFrameIndex = 0
        # the list of the frames to show to the user
        self.frameList = [HomeFrame(mainframe)]

        # foreach the frames in the list, forget the one that is currently not in the list
        for ix in range(len(self.frameList)):
            if(ix != self.activeFrameIndex):
                self.frameList[ix].forget()


#set up window

root = tk.Tk()
window = Window(root)
root.title('Todo Randomizer')


#run
root.mainloop()

