from tkinter import *
from functools import partial
from BDD.sqliteservice import *
from toolsbox import *
from VUES.entrycustom import EntryCustom
from VUES.windowcustom import WindowCustom
from VUES.optionmenucustom import OptionMenuCustom
from CONTROLLERS.matierecontroller import MatiereController

class MatiereForm():

    def __init__(self,master):
        self.master = master
        self.controller = MatiereController()

    def form_add_matiere(self):
        window = WindowCustom(self.master)

        entrys = {
            "Matiere":None,
        }

        container = Frame(window)
        EntryCustom(container,entrys,"Matiere")
        container.pack(fill=BOTH)

        btn = Button(window, text="Valider", command=partial(self.controller.addMatiere ,entrys)).pack(side=BOTTOM)

    def form_delete_matiere(self):
        window = WindowCustom(self.master)

        entrys = {
            "Matiere":None,
        }

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleMatiere FROM MATIERE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        OptionMenuCustom(container,listeOptions,entrys,"Matiere")
        container.pack(fill=BOTH)

        btn = Button(window, text="Valider", command=partial(self.controller.deleteMatiere ,entrys)).pack(side=BOTTOM)

