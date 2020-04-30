from tkinter import *

class WindowCustom(Toplevel):

    def __init__(self, master ):
        self.width = 200
        self.height = 200
        super().__init__(master=master, width=self.width, height=self.height)
        
        