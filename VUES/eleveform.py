from tkinter import *
from functools import partial
from BDD.sqliteservice import *
from toolsbox import *
from CONTROLLERS.elevecontroller import EleveController
from VUES.windowcustom import WindowCustom
from VUES.optionmenucustom import OptionMenuCustom
from VUES.entrycustom import EntryCustom

class EleveForm():        
        
    def __init__(self,master):
        self.master = master
        self.controller = EleveController()
    
    #Prend en paramètre une liste d'attribut, le nom de l'entité voulu (Eleve, MAtiere ..), retourne les entrées d'utilisateur
    def form_add_eleve(self):
        window = WindowCustom(self.master)

        entrys = {
            "Nom":None,
            "Prenom":None,
            "Classe":None
        }
        
        container = Frame(window)
        EntryCustom(container,entrys,"Nom")
        container.pack(fill=BOTH)

        container = Frame(window)
        EntryCustom(container,entrys,"Prenom")
        container.pack(fill=BOTH)

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleClasse FROM CLASSE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"Classe").pack()
        container.pack(fill=BOTH)

        btn = Button(window, text="Valider", command=partial(self.controller.addEleve ,entrys)).pack(side=BOTTOM)


    @staticmethod
    def refreshEleve(*args,entrys, optionEleves):
        listOptions = SqliteService.getInstance().selectByQueryEntity("SELECT a.prenomApprenant || ' ' || a.nomApprenant AS fullname FROM APPRENANT AS a INNER JOIN CLASSE AS cls ON a.idClasse = cls.idClasse WHERE cls.libelleClasse = '{0}'".format(entrys["Classe"].get()))
        listOptions = ToolsBox.convert_rowlist_tostringlist(listOptions)
        optionEleves.refresh(listOptions)

    def form_delete_eleve(self):
        window = WindowCustom(self.master)

        entrys = {
            "Eleves":None,
            "Classe":None
        }

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleClasse FROM CLASSE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"Classe")
        optionClasse.pack(side=RIGHT)
        container.pack(fill=BOTH)

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT a.prenomApprenant || ' ' || a.nomApprenant AS fullname FROM APPRENANT AS a INNER JOIN CLASSE AS cls ON a.idClasse = cls.idClasse WHERE cls.libelleClasse = '{0}'".format(entrys["Classe"].get()))
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionEleves = OptionMenuCustom(container,listeOptions,entrys,"Eleves")
        optionEleves.pack(side=RIGHT)
        container.pack(fill=BOTH)

        optionClasse.v.trace("w",partial(EleveForm.refreshEleve,entrys=entrys,optionEleves=optionEleves))
        btn = Button(window, text="Valider", command=partial(self.controller.deleteEleve ,entrys)).pack(side=BOTTOM)

    def from_associate_eleve(self):
        window = WindowCustom(self.master)

        entrys = {
            "Eleves":None,
            "NewClasse":None
        }
        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT prenomApprenant || ' ' || nomApprenant AS fullname FROM APPRENANT ORDER BY nomApprenant")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"Eleves")
        optionClasse.pack(side=RIGHT)
        container.pack(fill=BOTH)

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleClasse FROM CLASSE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"NewClasse")
        optionClasse.pack(side=RIGHT)
        container.pack(fill=BOTH)

        btn = Button(window, text="Valider", command=partial(self.controller.associateEleveWithClasse ,entrys)).pack(side=BOTTOM)

    def from_display_eleve(self):
        window = WindowCustom(self.master)

        entrys = {
            "Enseignant":None,
            "Matiere":None
        }

        listeEleve = SqliteService.getInstance().selectByQueryEntity("SELECT prenomApprenant || ' ' || nomApprenant AS fullname FROM APPRENANT")
        listeEleve = ToolsBox.convert_rowlist_tostringlist(listeEleve)
        scrollbar = Scrollbar(window)
        scrollbar.pack(side = RIGHT, fill = Y)
        listEleve = Listbox(window, yscrollcommand=scrollbar.set)
        for eleve in listeEleve:
            listEleve.insert(END, eleve)
        listEleve.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command = listEleve.yview)


        
        

