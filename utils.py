import tkinter as tk
import utils
from Task import Task
from Category import Category
from CategoryFrame import CategoryFrame
from functools import partial
import json
from tkinter import ttk
import re
from datetime import datetime as dt

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

    # remove all CategoryFrames from frame_list
    for frame in utils.frame_list:
        if(isinstance(frame, CategoryFrame)):
            utils.frame_list.remove(frame)

    # remove all categories from saved_categories
    utils.saved_categories = {}

    # todo for each category, get the corresponding task
    for ix in range(len(result)):

        # check the key 'name' exist
        if(not 'name' in result[ix]):
            raise Exception('the key \"name\" could not be found for a category')
        
        name = result[ix]['name']

        # check the key 'currentTask' exist
        if(not 'currentTask' in result[ix]):
            raise Exception(f'the key \"currentTask\" could not be found for the category named \"{name}\"')
        
        # check the key 'backloggedTasks' exist
        if(not 'backloggedTasks' in result[ix]):
            raise Exception(f'the key \"backloggedTasks\" could not be found for the category named \"{name}\"')
        
        # check the key 'completeTasks' exist
        if(not 'completeTasks' in result[ix]):
            raise Exception(f'the key \"completeTasks\" could not be found for the category named \"{name}\"')
        
        

        # verify that name is a string
        if(not isinstance(name, str)):
            raise Exception(f"Name of a category must be a string (given \"{name}\")")


        # verify the name (trimmed) is not empty
        if(name.strip() == ""):
            raise Exception("Name can't be an empty str")
        

        # verity the name (trimmed, upper) is not the same as any other names
        for saved_category_name in utils.saved_categories:
            name_check = name.strip()
            if(saved_category_name.upper() == name_check.upper()):
                raise Exception(f"Categories can't have duplicate names (given \"{name_check}\")")        

        category = Category(name.strip())

        # check that the current task is valid
        current_task_dict = result[ix]['currentTask']
        if(current_task_dict is not None):
            valid_task(task=current_task_dict, current_task=None, backlogged_tasks=[], complete_tasks=[])
            current_task = Task(current_task_dict['name'].strip())
            current_task.start_date = current_task_dict['startDate']
            current_task.end_date = current_task_dict['endDate']
            category.current_task = current_task

        else:
            category.current_task = None

        # check that the tasks in the backlog are valid
        for backlogged_task_dict in result[ix]['backloggedTasks']:
            valid_task(task=backlogged_task_dict, current_task=category.current_task, backlogged_tasks=category.backlogged_tasks, complete_tasks=[])
            task = Task(backlogged_task_dict['name'].strip())
            task.start_date = backlogged_task_dict['startDate']
            task.end_date = backlogged_task_dict['endDate']
            category.add_task_to_backlog(task)
       
        # check that the tasks in the complete task are valid
        for complete_task_dict in result[ix]['completeTasks']:
            valid_task(task=complete_task_dict, current_task=category.current_task, backlogged_tasks=category.backlogged_tasks, complete_tasks=category.complete_tasks)
            task = Task(complete_task_dict['name'].strip())
            task.start_date = complete_task_dict['startDate']
            task.end_date = complete_task_dict['endDate']

        # add the new category to the list of saved categories
        utils.saved_categories.update({category.name: category})


# Tells if a task is valid or not
def valid_task(task, current_task, backlogged_tasks, complete_tasks):
    # verify that the key "name" exists in the dictionary
    if(not 'name' in task):
        raise Exception(f'The key \"name\" could not be found for a task')
    name = task['name']

    # verify that the key "startDate" exists in the dictionary
    if(not 'startDate' in task):
        raise Exception(f'The key \"startDate\" could not be found for a task named \"{name}\"')
    start_date = task['startDate']
    
    # verify that the key "endDate" exists in the dictionary
    if(not 'endDate' in task):
            raise Exception(f'The key \"endDate\" could not be found for a task named \"{name}\"')
    end_date = task['endDate']
    
    # the name of the task must be a string
    if(not isinstance(name, str)):
        raise Exception(f"task name must be a string (given \"{name}\")")

    # the name of the task can't be empty
    if(name.strip() == ""):
        raise Exception(f"task name not be an empty string")

    # start date must be a string
    if(not isinstance(start_date, str)):
        raise Exception(f"start date must be a string (given \"{start_date}\")")
    
    # end date must be a string
    if(not isinstance(end_date, str)):
        raise Exception(f"end date must be a string (given \"{end_date}\")")
    
    start_date_matches = re.search("^(\\d{2})-(\\d{2})-(\\d{4})$", start_date)
    end_date_matches = re.search("^(\\d{2})-(\\d{2})-(\\d{4})$", end_date)
    
    # the start date must either be "None" or in the format "MM-DD-YYYY"
    if(start_date != "None" and not start_date_matches):
        raise Exception(f"start date must either be \"None\" or in the format \"MM-DD-YYYY\" (given \"{start_date}\")")
            
    # the end date must either be "None" or in the format "MM-DD-YYYY"
    if(end_date != "None" and not end_date_matches):
        raise Exception("end date must either be \"None\" or in the format \"MM-DD-YYYY\"")

    # if end_date is not "None" then start_date must not be "None"
    if(end_date != "None" and start_date == "None"):
        raise Exception(f"start date must not be \"None\" if end date is not \"None\" (given end date is \"{end_date}\")")
    
    # check to make sure the end date is not before the start date (if the stat and end date are not None)
    if(start_date != "None" and end_date != "None"):
        start_date_dt = dt(int(start_date_matches.group(3)), int(start_date_matches.group(1)), int(start_date_matches.group(2)))
        end_date_dt = dt(int(end_date_matches.group(3)), int(end_date_matches.group(1)), int(end_date_matches.group(2)))
        if(end_date_dt < start_date_dt):
            raise Exception(f"The start date ({start_date}) cannot be after the end date ({end_date})")

    name_check = name.strip().upper()
    # verify all the names within the backlog are not the same
    for backlogged_task in backlogged_tasks:
        if(name_check == backlogged_task.name.upper()):
            raise Exception(f"task name must not be the same of another task within backlog (task name given \"{backlogged_task.name}\")")
    
    # verify all the names within the completed task list are not the same
    for complete_task in complete_tasks:
        if(name_check == complete_task.name.upper()):
            raise Exception(f"task name must not be the same of another task within the complete task list (task name given \"{complete_task.name}\")")

    # if the current task is not None, verify that it doesn't share a name with
    if (current_task is not None and name_check == current_task.name.upper()):
        raise Exception(f"task name must not be the same of current task \"{current_task.name}\"")

