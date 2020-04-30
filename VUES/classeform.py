from tkinter import *
from functools import partial
from BDD.sqliteservice import *
from toolsbox import *
from CONTROLLERS.classecontroller import ClasseController
from VUES.windowcustom import WindowCustom
from VUES.optionmenucustom import OptionMenuCustom
from VUES.entrycustom import EntryCustom

class ClasseForm():        
        
    def __init__(self,master):
        self.master = master
        self.controller = ClasseController()

    @staticmethod
    def refreshClasse(*args,entrys,listbox):
        listbox.delete(0,END)

        queryToShowEleve = """SELECT a.prenomApprenant || ' ' || a.nomApprenant
                    FROM APPRENANT AS a
                    INNER JOIN CLASSE AS c ON a.idClasse = c.idClasse
                    WHERE c.libelleClasse = '{0}'""".format(entrys["Classe"].get())
        
        listOptions = SqliteService.getInstance().selectByQueryEntity(queryToShowEleve)
        listOptions = ToolsBox.convert_rowlist_tostringlist(listOptions)

        for eleve in listOptions:
            listbox.insert(END, eleve)

    def form_display_byclasse(self):
        window = WindowCustom(self.master)

        entrys = {
            "Classe":None
        }

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleClasse FROM CLASSE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"Classe")
        optionClasse.pack(side=LEFT)
        container.pack()

        container = Frame(window)
        listeEleve = SqliteService.getInstance().selectByQueryEntity("SELECT a.prenomApprenant || ' ' || a.nomApprenant FROM APPRENANT AS a INNER JOIN CLASSE AS c ON a.idClasse = c.idClasse WHERE c.libelleClasse = '{0}'".format(entrys["Classe"].get()))
        listeEleve = ToolsBox.convert_rowlist_tostringlist(listeEleve)
        scrollbar = Scrollbar(window)
        scrollbar.pack(side = RIGHT, fill = Y)
        listEleveView = Listbox(window, yscrollcommand=scrollbar.set)
        for eleve in listeEleve:
            listEleveView.insert(END, eleve)
        listEleveView.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command = listEleveView.yview)
        container.pack(fill=BOTH)

        optionClasse.v.trace("w", partial(ClasseForm.refreshClasse, entrys=entrys,listbox=listEleveView))
