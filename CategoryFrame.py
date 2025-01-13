import tkinter as tk
from functools import partial
import utils

class CategoryFrame(tk.Frame):
    def __init__(self, categoryName, parent):
        super().__init__(parent)
        utils.make_label(f"\"{categoryName}\" category", self)
        self.parent = parent
        self.categoryName = categoryName
        self.create_frame()

    def create_frame(self):
        self.pack()