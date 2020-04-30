from tkinter import *

class EntryCustom(Entry):

    def __init__(self, master , entrys, nomEntry):
        self.width_entry = 30
        super().__init__(master, width=self.width_entry)
        entrys[nomEntry] = self
        Label(master, text= nomEntry).pack(side=LEFT)
        self.pack(side=LEFT)
        