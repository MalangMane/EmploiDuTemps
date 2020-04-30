from tkinter import *

class OptionMenuCustom(OptionMenu):

    def __init__(self,master, listOption,entrys , nomEntry):
        self.listOptions = listOption
        self.v = StringVar()
        self.v.set(self.listOptions[0])
        entrys[nomEntry] = self.v
        Label(master, text= nomEntry).pack(side=LEFT)
        super().__init__(master, self.v ,*self.listOptions)
        self.pack(side=LEFT)

    def refresh(self, newListOptions):
        self.v.set("")
        self['menu'].delete(0,'end')
        for option in newListOptions:
            self['menu'].add_command(label=option, command=lambda value=option: self.v.set(value))