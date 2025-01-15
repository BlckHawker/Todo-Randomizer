import tkinter as tk
import utils
from Task import Task
from Category import Category
from functools import partial
import json
from tkinter import ttk
import re

file_name = 'data.json'

# todo make it so saved_categories loads from a local json file
# todo make this a dictionary with the key being the name and the value being the Category object
saved_categories = {}


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

def export_data():
    new_list = [utils.saved_categories[category_name].export() for category_name in utils.saved_categories]
    file = open(file_name, 'w')
    json.dump(new_list, file, indent=4)
    file.close()

def import_data():
    file_name = 'data.json'
    file = open(file_name, 'r')
    result = json.load(file)
    file.close()
    print(result)

    # todo for each category, get the corresponding task
    for ix in range(len(result)):
        name = result[ix].name

        # todo verify that name is a string
        if(not isinstance(name, str)):
            raise Exception("Name must be a string")

        # todo check if this is needed given the first if statement
        # todo verify that the name is not None
        if(name is None):
            raise Exception("Name can't be None")


        # todo verify the name (trimmed) is not empty
        if(name.strip() != ""):
            raise Exception("Name can't be an empty str")
        

        # todo verity the name (trimmed, upper) is not the same as any other names
        for saved_category in utils.saved_categories:
            if(any(category.name.upper() == name.trim().upper() for category in saved_category)):
                    raise Exception("Categories can't have duplicate names")        

        category = Category(name.strip())

        {
            "name": "n",
            "startDate": "None",
            "endDate": "None"
        }


        # todo check that the current task is valid
        current_task = result[ix].currentTask
        if(current_task is not None):
            valid_task(name=current_task.name, start_date=current_task.startDate, end_date=current_task.endDate, backlogged_tasks= category.backlogged_tasks, complete_tasks=category.complete_tasks, current_task=None)
            new_current_task = Task(current_task.name.strip())
            new_current_task.start_date = current_task.startDate
            new_current_task.end_date = current_task.endDate
            category.current_task = new_current_task

        else:
            category.current_task = None

        # todo check that the tasks in the backlog are valid
        for backlogged_task in result[ix].backloggedTasks:
            valid_task(name=backlogged_task.name, start_date=backlogged_task.startDate, end_date=backlogged_task.endDate, backlogged_tasks= category.backlogged_tasks, complete_tasks=category.complete_tasks, current_task=category.current_task)
            task = Task(backlogged_task.name.strip())
            task.start_date = backlogged_task.startDate
            task.end_date = backlogged_task.endDate
            category.add_task_to_backlog(task)

        # todo check that the tasks in the complete task are valid
        for complete_task in result[ix].completeTasks:
            valid_task(name=complete_task.name, start_date=complete_task.startDate, end_date=complete_task.endDate, backlogged_tasks= category.backlogged_tasks, complete_tasks=category.complete_tasks, current_task=category.current_task)
            task = Task(complete_task.name.strip())
            task.start_date = complete_task.startDate
            task.end_date = complete_task.endDate
            category.complete_tasks.append(task)
        
        # todo test this
        utils.saved_categories.update({category.name: category})


# Tells if a task is valid or not
def valid_task(name, start_date, end_date, backlogged_tasks, complete_tasks, current_task):
    # todo the name of the task must be a string
    if(not isinstance(name, str)):
        raise Exception("name must be a string")
   

    # todo the name of the task can't be null 
    # todo (this check might be redundant by the check above)
    if(name is None):
        raise Exception("name must be a string")

    # todo the name of the task can't be empty
    if(name.strip() == ""):
        raise Exception("name must be a string")

    # todo start date must be a string
    if(not isinstance(start_date, str)):
        raise Exception("start date must be a string")
    
    # todo end date must be a string
    if(not isinstance(end_date, str)):
        raise Exception("end date must be a string")
    
    # todo the start date must either be "None" or in the format "MM-DD-YYYY"
    if(start_date != "None" and not re.search("^\d{2}-\d{2}-\d{4}$", start_date)):
        raise Exception("start date must either be \"None\" or in the format \"MM-DD-YYYY\"")
            
    # todo the end date must either be "None" or in the format "MM-DD-YYYY"
    if(end_date != "None" and not re.search("^\d{2}-\d{2}-\d{4}$", end_date)):
        raise Exception("end date must either be \"None\" or in the format \"MM-DD-YYYY\"")
    

    # todo if end_date is not "None" then start_date must not be "None"
    if(end_date != "None" and start_date == "None"):
        raise Exception("start date must not be \"None\" if end date is not \"None\"")
    
    tasks = []

    name_check = name.trim().upper()
    # todo verify all the names within the backlog are not the same
    if any(name_check == task.name.upper() for task in backlogged_tasks):
        raise Exception("task name must not be the same of another task within backlog")
    
    # todo verify all the names within the completed task list are not the same
    if any(name_check == task.name.upper() for task in complete_tasks):
        raise Exception("task name must not be the same of another task within the complete task list")

    # todo if the current task is not None, verify that it doesn't share a name with
    if (current_task is not None and name_check == current_task.name.upper()):
        raise Exception("task name must not be the same of current task")

