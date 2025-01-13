import tkinter as tk
from tkinter import ttk
from HomeFrame import HomeFrame
from CategoryFrame import CategoryFrame
import utils
# The window created to show a Frame to a use
class MainFrame():
    def __init__(self, master):
        mainframe = tk.Frame(master)
        mainframe.pack()

        self.homeFrame = HomeFrame(mainframe)
        # the index of the frame that is currently shown to the user
        self.activeFrameIndex = 0
        # the list of the frames to show to the user
        utils.frame_list = [self.homeFrame]

        # add the categories 
        # todo this is where categories would be loaded from the json
        for name in utils.saved_categories_names:
            utils.frame_list.append(CategoryFrame(name, mainframe))

        print(len(utils.frame_list))

        # foreach the frames in the list, forget the one that is currently not in the list
        for frame in utils.frame_list:
            if(frame != self.homeFrame):
                frame.forget()

    def change_window(self, frame: tk.Frame):
        # make it so the current frame is disabled
        utils.frame_list[self.activeFrameIndex].forget()

        #todo enable to new frame

        #todo change the active frame index

    def remove_category_frame(self, name):
        pass
        

    

#set up window
root = tk.Tk()
window = MainFrame(root)
root.title('Todo Randomizer')

#run
root.mainloop()

