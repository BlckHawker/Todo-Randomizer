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
        
        utils.active_frame_index = 0
        # the list of the frames to show to the user
        utils.frame_list = [self.homeFrame]

        
        
        # foreach the frames in the list, forget the one that is currently not in the list
        for frame in utils.frame_list:
            if(frame != self.homeFrame):
                frame.forget()

        self.homeFrame.update_frame()

    
    
#set up window
root = tk.Tk()
window = MainFrame(root)
root.title('Todo Randomizer')

#run
root.mainloop()

