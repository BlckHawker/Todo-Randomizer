import tkinter as tk
from functools import partial
import utils

class CategoryFrame(tk.Frame):
    def __init__(self, category_name, parent):
        super().__init__(parent)
        utils.make_label(f"\"{category_name}\" category", self)
        self.parent = parent
        self.category_name = category_name

    def create_frame(self):
        self.pack()