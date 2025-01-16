import tkinter as tk
from tkinter import ttk
from functools import partial
import utils
from CategoryFrame import CategoryFrame
from Category import Category

# The home page that will show the categories
class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        utils.make_label('Categories', self)
        self.parent = parent
        self.update_frame()
        

    # When this button is clicked, delete the category from the list
    def delete_category(self, category_name: str):
        del utils.saved_categories[category_name]
        self.update_frame()

        #remove the CategoryFrame
        for frame in utils.frame_list:
            if (isinstance(frame, CategoryFrame) and frame.category_name == category_name):
                frame_to_remove = frame
                utils.frame_list.remove(frame_to_remove)
                break

        # When this button is clicked, open a window to show the new category window
    def select_category(self, category: str):
        desired_frame = [frame for frame in utils.frame_list if isinstance(frame, CategoryFrame) and frame.category.name ==  category][0]
        if(desired_frame is None):
            raise Exception('desired_frame not found')
        utils.change_window(desired_frame)

    def update_frame(self):
        # forget all children if they exist (except any pop ups)
        for widget in self.winfo_children():
            if(not isinstance(widget, tk.Toplevel)):
                widget.destroy()

        self.pack_forget()

        utils.make_label(text="Categories", master=self)

        #if there are no categories, make a label to show that
        #otherwise, list the categories with their own label
        if(len(utils.saved_categories) == 0):
            category_frame = ttk.Frame(master=self)
            category_frame.pack()
            utils.make_label(text='N/A', master=category_frame, side='left', padx=10)
        else:
            utils.organize_saved_categories()
            for category_name in utils.saved_categories:
                category_frame = ttk.Frame(master=self)
                category_frame.pack()
                utils.make_label(category_name, category_frame, side='left', padx=10)
                utils.make_button('Select', category_frame, side='left', padx=10, command=partial(self.select_category, category_name))
                utils.make_button('Delete', category_frame, side='left', padx=10, command=partial(self.delete_category, category_name))

        button_frame = ttk.Frame(self)
        button_frame.pack()
        utils.make_button('Add Category', button_frame, command=self.add_category_button_press, side="left")
        utils.make_button('Export Data', master=button_frame, command=partial(utils.export_data), side="left")
        utils.make_button('Import Data', master=button_frame, command=partial(self.import_data), side="left")
        self.pack()

    def add_category_button_press(self):
        utils.create_pop_up_with_input(master=self, label_text="Choose the name of the new category:", button_method=self.submit_category_check)
    
    def submit_category_check(self, entryStr, warning_label):
        # get the trimmed input
        input = entryStr.get().strip()

        warningText = ""

        # input can't be empty
        if(input == ""):
            warningText = "input can't be empty"
        # input can't already be in saved_categories
        elif(any(category.upper() == input.upper() for category in utils.saved_categories)):
            warningText = f"\"{input}\" is already a category"

        # add the new category to the list if valid
        if(warningText == ""):

            utils.saved_categories.update({input: Category(input)})
            warningText = f"Added \"{input}\" as new category"
            warning_label.config(foreground="green")
            self.update_frame()
            category_frame = CategoryFrame(input, self.parent)
            utils.frame_list.append(category_frame)
            category_frame.forget()

        else:
            warning_label.config(foreground="red")
        
        warning_label.pack()
        warning_label.config(text = warningText)

    def import_data(self):
        # import the data
        utils.import_data()
        # todo update the frame
        self.update_frame()