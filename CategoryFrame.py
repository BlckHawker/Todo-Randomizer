import tkinter as tk
from tkinter import ttk
from functools import partial
from Category import Category
from Task import Task
import utils

class CategoryFrame(tk.Frame):
    def __init__(self, category_name, parent):
        super().__init__(parent)
        self.parent = parent
        self.category_name = category_name
        self.category = utils.saved_categories[category_name]


        current_task = self.category.current_task
        backlogged_tasks = self.category.backlogged_tasks

        # Category Name label
        utils.make_label(f"\"{category_name}\" category", self)

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
        # todo give this functionality
        self.add_button = utils.make_button(text='Add Task', master=button_frame, side='left')

        # back to home button 
        utils.make_button(text="Back to Home", master=self, command=partial(self.go_to_home_frame))

    # shows this frame
    def show_frame(self):
        self.pack()

    # Go back to the Home frame
    def go_to_home_frame(self):
        # the first index of frame_list should be the home frame
        utils.change_window(utils.frame_list[0])