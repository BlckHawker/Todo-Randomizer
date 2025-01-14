import tkinter as tk
from tkinter import ttk
from functools import partial
from Category import Category
from Task import Task
import utils

class CategoryFrame(tk.Frame):
    def __init__(self, category_name, parent):
        super().__init__(parent)
        self.category = utils.saved_categories[category_name]
        self.update_frame()

    # shows this frame
    def show_frame(self):
        self.pack()

    # Go back to the Home frame
    def go_to_home_frame(self):
        # the first index of frame_list should be the home frame
        utils.change_window(utils.frame_list[0])

    # Add a task to the back log of a category
    def add_task(self):
        utils.create_pop_up_with_input(self, "Choose the name of the new task:", self.submit_task_check)


    # function to check the new task added to backlog is valid
    def submit_task_check(self, entryStr, warning_label):
        # get the trimmed input
        input = entryStr.get().strip()
        warningText = ""

        # input can't be empty
        if(input == ""):
            warningText = "input can't be empty"

        # input can't be the name of the current task
        elif(self.category.current_task is not None and self.category.current_task.name.upper() == input.upper()):
            warningText = "input can't be the name of the current task"
        
        # input can't be the name of a task in the back log
        else:
            for task in self.category.backlogged_tasks:
                if(task.name.upper() == input.upper()):
                    warningText = "input can't be the name of a task in the backlog"
                    break

        # add the task to the back log of the task
        if(warningText == ""):
            self.category.add_task_to_backlog(Task(input))
            warningText = f'Added \"{input}\" as a new back logged task'
            warning_label.config(foreground="green")

        else:
            warning_label.config(foreground="red")
        
        warning_label.pack()
        warning_label.config(text = warningText)
        self.update_frame()
        self.show_frame()

    def update_frame(self):
        # forget all children if they exist (except any pop ups)
        for widget in self.winfo_children():
            if(not isinstance(widget, tk.Toplevel)):
                widget.destroy()

        self.pack_forget()

        current_task = self.category.current_task
        backlogged_tasks = self.category.backlogged_tasks
        # Category Name label
        utils.make_label(f"\"{self.category.name}\" category", self)

        # Current task label
        self.current_task_label = utils.make_label(text=f'Current task: {"N/A" if current_task is None else current_task}', master=self)

        b_frame = ttk.Frame(self)

        # Set current task as complete button
        # todo give this functionality
        self.current_task_complete_button = utils.make_button(text='Set as complete', master=b_frame, side='left')

        # remove current task as current task
        # todo give this functionality
        utils.make_button(text='Remove as current task', master=b_frame, side='left')


        # if the current_task is t none, make the button invisible
        if(current_task is None):
            self.current_task_complete_button.forget()

        # backlogged tasks frame
        backlogged_tasks_frame = ttk.Frame(self)
        backlogged_tasks_frame.pack()

        # backlogged tasks label
        self.backlogged_tasks_label = utils.make_label(text='Backlogged Tasks', master=backlogged_tasks_frame)
        self.backlogged_tasks_label.pack()

        # add the list of backlogged tasks
        if(len(backlogged_tasks) == 0):
            utils.make_label(text='N/A', master=self)
        else:
            # sort the backlogged tasks
            self.category.backlogged_tasks.sort(key=lambda task: task.name)
            for task in backlogged_tasks:
                frame = ttk.Frame(master=backlogged_tasks_frame)
                frame.pack()
                utils.make_label(text=task.name, master=frame, side='left')
                # todo give this functionality
                utils.make_button(text='Set as current task', master=frame, side='left')

                # todo give this functionality
                utils.make_button(text='Delete Task', master=frame, side='left')

        button_frame = ttk.Frame(self)
        button_frame.pack()
        # todo give this functionality
        # randomly assign task button
        self.randomly_assign_task_button = utils.make_button(text='Randomly assign current task', master=button_frame, side='left')
        
        # add task button
        self.add_button = utils.make_button(text='Add Task', master=button_frame, side='left', command=partial(self.add_task))

        # back to home button 
        utils.make_button(text="Back to Home", master=self, command=partial(self.go_to_home_frame))
