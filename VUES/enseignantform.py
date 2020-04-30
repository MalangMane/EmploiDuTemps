from tkinter import *
from functools import partial
from BDD.sqliteservice import *
from toolsbox import *
from VUES.entrycustom import EntryCustom
from VUES.windowcustom import WindowCustom
from VUES.optionmenucustom import OptionMenuCustom
from CONTROLLERS.enseignantcontroller import EnseignantController

class EnseignantForm():

    def __init__(self,master):
        self.master = master
        self.controller = EnseignantController()


    def form_add_enseignant(self):
        window = WindowCustom(self.master)

        entrys = {
            "Nom":None,
            "Prenom":None
        }

        container = Frame(window)
        EntryCustom(container,entrys,"Nom")
        container.pack(fill=BOTH)

        container = Frame(window)
        EntryCustom(container,entrys,"Prenom")
        container.pack(fill=BOTH)

        btn = Button(window, text="Valider", command=partial(self.controller.addEnseignant ,entrys)).pack(side=BOTTOM)


    def form_delete_enseignant(self):
        window = WindowCustom(self.master)

        entrys = {
            "Enseignant":None
        }

        container= Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT prenomEnseignant || ' ' || nomEnseignant AS fullname FROM ENSEIGNANT")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionEnseignant = OptionMenuCustom(container,listeOptions,entrys,"Enseignant")
        container.pack()

        btn = Button(window, text="Valider", command=partial(self.controller.deleteEnseignant ,entrys)).pack(side=BOTTOM)


    def form_associate_matiere(self):
        window = WindowCustom(self.master)

        entrys = {
            "Enseignant":None,
            "Matiere":None
        }

        Label(window , text="(Sélectionner dans le liste, l'enseignant puis la matiere, puis validez)").pack(side=TOP)
        container = Frame(window)
        listeOptions = SqliteService.getInstance().selectByQueryEntity("SELECT prenomEnseignant || ' ' || nomEnseignant AS fullname FROM ENSEIGNANT")
        listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
        optionEnseignant = OptionMenuCustom(container,listeOptions,entrys,"Enseignant")
        container.pack()

        container = Frame(window)
        listeMatiere = SqliteService.getInstance().selectByQueryEntity("SELECT libelleMatiere FROM MATIERE")
        listeMatiere = ToolsBox.convert_rowlist_tostringlist(listeMatiere)
        optionMatiere = OptionMenuCustom(container,listeMatiere,entrys,"Matiere")
        container.pack()

        btn = Button(window, text="Valider", command=partial(self.controller.associateEnseignantMatiere ,entrys)).pack(side=BOTTOM)

    def form_display_enseignant(self):
        window = WindowCustom(self.master)
        #FROM MATIERE_ENSEIGNANT AS m_e INNER JOIN ENSEIGNANT AS e ON m_e.k_idEnseignant = e.idEnseignant INNER JOIN MATIERE AS mat ON m_e.k_idMatiere = mat.idMatiere
        listeEnseignant = SqliteService.getInstance().selectByQueryEntity("SELECT prenomEnseignant || ' ' || nomEnseignant AS fullname FROM ENSEIGNANT")
        listeEnseignant = ToolsBox.convert_rowlist_tostringlist(listeEnseignant)

        for enseignant in listeEnseignant:
            print(enseignant)
            container = Frame(window)
            nomPrenomEnseignant = enseignant.split()
            query = "SELECT mat.libelleMatiere FROM MATIERE_ENSEIGNANT AS m_e INNER JOIN ENSEIGNANT AS e ON m_e.k_idEnseignant = e.idEnseignant INNER JOIN MATIERE AS mat ON m_e.k_idMatiere = mat.idMatiere WHERE e.nomEnseignant = '{0}' AND e.prenomEnseignant = '{1}'".format(nomPrenomEnseignant[1], nomPrenomEnseignant[0])
            listeMatiereRow = SqliteService.getInstance().selectByQueryEntity(query)
            matieres = "("
            for matiereRow in listeMatiereRow:
                matieres += matiereRow["libelleMatiere"] + " / "
            matieres += ")"
            Label(container, text=enseignant).pack(side=LEFT)
            Label(container, text=matieres).pack(side=RIGHT)
            container.pack(fill=BOTH)
        

