import tkinter as tk
from tkinter import ttk
from functools import partial
import utils
from CategoryFrame import CategoryFrame;
# The home page that will show the categories
class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        utils.make_label('Categories', self)
        self.parent = parent
        self.create_frame_categories()
        

    # When this button is clicked, delete the category from the list
    def delete_category(self, category: str):
        utils.saved_categories_names.remove(category)
        self.create_frame_categories()

        #remove the CategoryFrame
        print(f'before deletion {len(utils.frame_list)}')
        for frame in utils.frame_list:
            if (isinstance(frame, CategoryFrame) and frame.categoryName == category):
                frame_to_remove = frame
                utils.frame_list.remove(frame_to_remove)
                break
        print(f'after deletion {len(utils.frame_list)}')

    def select_category(self, category: str):
        print(f'Select category "{category}"')
        # When this button is clicked, open a window to show the new category window

    def create_frame_categories(self):
        # forget all children if they exist (except any )
        for widget in self.winfo_children():
            if(not isinstance(widget, tk.Toplevel)):
                widget.destroy()

        self.pack_forget()

        utils.make_label(text="Categories", master=self)

        #if there are no categories, make a label to show that
        #otherwise, list the categories with their own label
        if(len(utils.saved_categories_names) == 0):
            category_frame = ttk.Frame(master=self)
            category_frame.pack()
            utils.make_label(text='N/A', master=category_frame, side='left', padx=10)
        else:
            utils.organize_saved_categories()
            for category in utils.saved_categories_names:
                category_frame = ttk.Frame(master=self)
                category_frame.pack()
                utils.make_label(category, category_frame, side='left', padx=10)
                utils.make_button('Select', category_frame, side='left', padx=10, command=partial(self.select_category, category))
                utils.make_button('Delete', category_frame, side='left', padx=10, command=partial(self.delete_category, category))

        utils.make_button('Add Category', self, command=self.add_category_button_press)
        self.pack()

    def add_category_button_press(self):
        top= tk.Toplevel(self)
        input_frame = ttk.Frame(top)
        input_frame.pack()
        utils.make_label(text= "Choose the name of the new category:", master=input_frame, side= 'left')
        entryStr = tk.StringVar()
        entry = ttk.Entry(input_frame, textvariable=entryStr)
        entry.pack()
        button_frame = ttk.Frame(top)
        button_frame.pack()
        # make a warning text that will pop up when the user inputs an invalid thing
        warning_label = utils.make_label(text="Warning label", master=top, foreground="red")
        warning_label.forget()
        utils.make_button(text="Cancel", master=button_frame, side= 'left', command=lambda: top.destroy()) # When the cancel button is clicked, close this window
        utils.make_button(text= "Submit", master=button_frame, side= 'left', command=partial(self.submit_category_check, entryStr, warning_label))
        
        top.transient(self) # set to be on top of the main window
        top.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
        self.wait_window(self) # pause anything on the main window until this one closes

    def submit_category_check(self, entryStr, warning_label):
        # get the trimmed input
        input = entryStr.get().strip()

        warningText = ""

        # input can't be empty
        if(input == ""):
            warningText = "input can't be empty"
        # input can't already be in saved_categories
        elif(any(category.upper() == input.upper() for category in utils.saved_categories_names)):
            warningText = f"\"{input}\" is already a category"

        # add the new category to the list if valid
        if(warningText == ""):
            utils.saved_categories_names.append(input)
            warningText = f"Added \"{input}\" as new category"
            warning_label.config(foreground="green")
            self.create_frame_categories()

        else:
            warning_label.config(foreground="red")
        

        warning_label.pack()
        warning_label.config(text = warningText)