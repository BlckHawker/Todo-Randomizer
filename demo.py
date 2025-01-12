import tkinter as tk
from tkinter import ttk
from  HomeFrame import HomeFrame
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

