from tkinter import *
from functools import partial
from BDD.sqliteservice import *
from toolsbox import *
from CONTROLLERS.courscontroller import *
from VUES.entrycustom import EntryCustom
from VUES.windowcustom import WindowCustom
from VUES.optionmenucustom import OptionMenuCustom
from CONTROLLERS.courscontroller import CoursController

class CoursForm():

    def __init__(self,master):
        self.master = master
        self.controller = CoursController()

    @staticmethod   
    def refreshMatiere(*args,entrys, optionMatiere):
        prenomNomEnseignant = entrys["Enseignant"].get().split()
        listOptions = SqliteService.getInstance().selectByQueryEntity("SELECT mat.libelleMatiere FROM MATIERE_ENSEIGNANT AS m_e INNER JOIN ENSEIGNANT AS e ON m_e.k_idEnseignant = e.idEnseignant INNER JOIN MATIERE AS mat ON m_e.k_idMatiere = mat.idMatiere WHERE e.nomEnseignant = '{0}' AND e.prenomEnseignant = '{1}'".format(prenomNomEnseignant[1], prenomNomEnseignant[0]))
        listOptions = ToolsBox.convert_rowlist_tostringlist(listOptions)
        optionMatiere.refresh(listOptions)


    def form_add_cours(self):
        window = WindowCustom(self.master)

        entrys = {
            "Jour":None,
            "Mois":None,
            "Annee":None,
            "Heure":None,
            "Classe":None,
            "Enseignant":None,
            "Matiere":None
        }
        container = Frame(window)
        Label(container,text="Jour").pack(side=LEFT)
        sb = Spinbox(container, from_=1, to=31, width=10, state="readonly")
        sb.pack(side=RIGHT)
        entrys["Jour"] = sb
        container.pack(fill=BOTH)

        container = Frame(window)
        Label(container,text="Mois").pack(side=LEFT)
        sb = Spinbox(container, from_=1, to=12, width=10, state="readonly")
        sb.pack(side=RIGHT)
        entrys["Mois"] = sb
        container.pack(fill=BOTH)

        container = Frame(window)
        Label(container,text="Année").pack(side=LEFT)
        sb = Spinbox(container, from_=2019, to=2022, width=10, state="readonly")
        sb.pack(side=RIGHT)
        entrys["Annee"] = sb
        container.pack(fill=BOTH)
        

        container = Frame(window)
        listOptions = ['AM','PM']
        OptionMenuCustom(container,listOptions,entrys,"Heure")
        container.pack(fill=BOTH)

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleClasse FROM CLASSE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"Classe")
        container.pack(fill=BOTH)

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT prenomEnseignant || ' ' || nomEnseignant AS fullname FROM ENSEIGNANT")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionEnseignant = OptionMenuCustom(container,listeOptions,entrys,"Enseignant")
        container.pack(fill=BOTH)

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleMatiere FROM MATIERE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionMatiere = OptionMenuCustom(container,listeOptions,entrys,"Matiere")
        container.pack(fill=BOTH)

        optionEnseignant.v.trace("w",partial(CoursForm.refreshMatiere,entrys=entrys,optionMatiere=optionMatiere))

        btn = Button(window, text="Valider", command=partial(self.controller.addCours ,entrys)).pack(side=BOTTOM)


    def form_update_cours(self):
        window = WindowCustom(self.master)

        entrys = {
            "Jour/Heure/Matiere":None,
            "Jour":None,
            "Heure":None,
            "Classe":None,
            "Enseignant":None,
            "Matiere":None
        }

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT crs.idCours ||'  '|| crs.jourCours ||' '|| crs.heureCours ||' '|| m.libelleMatiere AS jourHeureMatiere FROM COURS AS crs INNER JOIN MATIERE AS m ON crs.k_idMatiere = m.idMatiere")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"Jour/Heure/Matiere")
        container.pack(fill=BOTH)


        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleClasse FROM CLASSE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"Classe")
        container.pack(fill=BOTH)

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT prenomEnseignant || ' ' || nomEnseignant AS fullname FROM ENSEIGNANT")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionEnseignant = OptionMenuCustom(container,listeOptions,entrys,"Enseignant")
        container.pack(fill=BOTH)

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT libelleMatiere FROM MATIERE")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionMatiere = OptionMenuCustom(container,listeOptions,entrys,"Matiere")
        container.pack(fill=BOTH)

        optionEnseignant.v.trace("w",partial(CoursForm.refreshMatiere,entrys=entrys,optionMatiere=optionMatiere))

        btn = Button(window, text="Valider", command=partial(self.controller.updateCours ,entrys)).pack(side=BOTTOM)


    def form_delete_cours(self):
        window = WindowCustom(self.master)

        entrys = {
            "Jour/Heure/Matiere":None
        }

        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT crs.idCours ||'  '|| crs.jourCours ||' '|| crs.heureCours ||' '|| m.libelleMatiere AS jourHeureMatiere FROM COURS AS crs INNER JOIN MATIERE AS m ON crs.k_idMatiere = m.idMatiere")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionClasse = OptionMenuCustom(container,listeOptions,entrys,"Jour/Heure/Matiere")
        container.pack(fill=BOTH)

        btn = Button(window, text="Valider", command=partial(self.controller.deleteCours ,entrys)).pack(side=BOTTOM)