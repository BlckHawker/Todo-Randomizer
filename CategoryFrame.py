import tkinter as tk
from tkinter import ttk
from functools import partial
from Category import Category
from Task import Task
import utils
import random

class CategoryFrame(tk.Frame):
    def __init__(self, category_name, parent):
        super().__init__(parent)
        self.category = utils.saved_categories[category_name]
        self.show_complete_tasks = True 
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

        else:
            # input can't be the name of a task in the backlog
            for task in self.category.backlogged_tasks:
                if(task.name.upper() == input.upper()):
                    warningText = "input can't be the name of a task in the backlog"
                    break
            # input can't be the name of a task in the complete task list
            if(warningText == ""):
               for task in self.category.complete_tasks:
                if(task.name.upper() == input.upper()):
                    warningText = "input can't be the name of a task in the complete task list"
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
        self.update_frame(True)

    def update_frame(self, show_frame = False):
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
        self.current_task_label = utils.make_label(text=f'Current task: {"N/A" if current_task is None else current_task.name}', master=self)

        b_frame = ttk.Frame(self)

        # Set current task as complete button
        utils.make_button(text='Set as complete', master=b_frame, side='left', command=partial(self.set_as_complete))

        # remove current task as current task
        utils.make_button(text='Remove as current task', master=b_frame, side='left', command=partial(self.remove_as_current_task, self.category.current_task))

        # if the current_task is not none, make the buttons visible
        if(current_task is not None):
            b_frame.pack()

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
                utils.make_button(text='Set as current task', master=frame, side='left', command=partial(self.set_as_current_task, task))
                utils.make_button(text='Delete Task', master=frame, side='left', command=partial(self.delete_task, task))

        button_frame = ttk.Frame(self)
        button_frame.pack()
        # randomly assign task button
        randomly_assign_task_button = utils.make_button(text='Randomly assign current task', master=button_frame, side='left', command=partial(self.randomly_assign_current_task))

        # Do not show this button if there are no tasks in the backlog
        if(len(self.category.backlogged_tasks) <= 0):
            randomly_assign_task_button.forget()
        
        # add task button
        self.add_button = utils.make_button(text='Add Task', master=button_frame, side='left', command=partial(self.add_task))

        # back to home button 
        utils.make_button(text="Back to Home", master=self, command=partial(self.go_to_home_frame))


        # completed task label
        utils.make_label(text="Completed Tasks", master=self)

        # if there are no complete tasks, just show "N/A", otherwise show the tasks with the show/hide button 
        if(len(self.category.complete_tasks) == 0):
            utils.make_label(text="N/A", master=self)
        else:
            # show/hide complete tasks button
            utils.make_button(text= "Show" if self.show_complete_tasks else "Hide", master=self, command=partial(self.toggle_complete_tasks))
            if(self.show_complete_tasks):
                # sort the completed tasks
                self.category.complete_tasks.sort(key=lambda task: task.name)
                for task in self.category.complete_tasks:
                    utils.make_label(text=task.name, master=self)
                    # give the option to delete a complete task
                    utils.make_button(text="Remove task", master=self, command=partial(self.remove_complete_task, task))
                    utils.make_label(text=f"Start Date: {task.start_date}", master=self)
                    utils.make_label(text=f"End Date: {task.end_date}", master=self)

        # show the frame if asked to
        if(show_frame):
            self.show_frame()

    def delete_task(self, task):
        self.category.backlogged_tasks.remove(task)
        self.update_frame(True)

    def set_as_current_task(self, task):
        self.category.set_task_as_current_task(task)
        self.update_frame(True)

    def remove_as_current_task(self, task):
        # set the current task to None
        self.category.current_task = None

        # add the old current task to the backlog
        self.category.add_task_to_backlog(task)
        self.update_frame(True)
    
    def randomly_assign_current_task(self):
        # randomly get a task from the backlog
        new_current_task = self.category.backlogged_tasks[random.randint(0, len(self.category.backlogged_tasks) - 1)]

        # set the random task as the current task
        self.category.set_task_as_current_task(new_current_task)
        self.update_frame(True)

    def set_as_complete(self):
        self.category.add_task_as_complete()
        self.update_frame(True)
    
    def toggle_complete_tasks(self):
        self.show_complete_tasks = not self.show_complete_tasks
        self.update_frame(True)

    def remove_complete_task(self, task):
        self.category.remove_complete_task(task)
        self.update_frame(True)