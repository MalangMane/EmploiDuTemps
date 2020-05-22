import tkinter as tk
from functools import partial
from DB.sqliteservice import *
from VUES.courscomponents import *
from VUES.eleveform import EleveForm
from VUES.courform import CoursForm
from VUES.matiereform import MatiereForm
from VUES.enseignantform import EnseignantForm
from VUES.classeform import ClasseForm
from VUES.optionmenucustom import OptionMenuCustom
from CONTROLLERS.courscontroller import *
from toolsbox import *
from VUES.affichageemploidutemps import *


# Déclaration de l'application principale
root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
posx = 500
posy = 300


root.configure(bg='white')
root.geometry('{0}x{1}+{2}+{3}'.format(width, height, str(posx), str(posy)))


# MENUS
menubar = Menu(root, tearoff=0)
menuEleve = Menu(menubar, tearoff=0)

eleveForm = EleveForm(root)

menuEleve.add_command(label="Ajout d'un élève",
                      command=eleveForm.form_add_eleve)
menuEleve.add_command(label="Suppresion d'un élève",
                      command=eleveForm.form_delete_eleve)
menuEleve.add_command(label="Association d'un élève à une classe",
                      command=eleveForm.from_associate_eleve)
menuEleve.add_command(label="Afficher les élèves",
                      command=eleveForm.from_display_eleve)
menubar.add_cascade(label="Eleve", menu=menuEleve)


menuCours = Menu(menubar, tearoff=0)
coursForm = CoursForm(root)
menuCours.add_command(label="Ajout d'un cours",
                      command=coursForm.form_add_cours)
menuCours.add_command(label="Suppression d'un cours",
                      command=coursForm.form_delete_cours)
menuCours.add_command(label="Modification d'un cours",
                      command=coursForm.form_update_cours)
menubar.add_cascade(label="Cours", menu=menuCours)


menuMatiere = Menu(menubar, tearoff=0)
matiereForm = MatiereForm(root)
menuMatiere.add_command(label="Ajout d'une matière",
                        command=matiereForm.form_add_matiere)
menuMatiere.add_command(label="Suppression d'une matière",
                        command=matiereForm.form_delete_matiere)
menubar.add_cascade(label="Matiere", menu=menuMatiere)


menuEnseignant = Menu(menubar, tearoff=0)
enseignantForm = EnseignantForm(root)
menuEnseignant.add_command(
    label="Ajout d'un enseignant", command=enseignantForm.form_add_enseignant)
menuEnseignant.add_command(label="Association d'un enseignant",
                           command=enseignantForm.form_associate_matiere)
menuEnseignant.add_command(
    label="Suppresion d'un enseignant", command=enseignantForm.form_delete_enseignant)
menuEnseignant.add_command(label="Afficher liste des enseignants",
                           command=enseignantForm.form_display_enseignant)
menubar.add_cascade(label="Enseignant", menu=menuEnseignant)

menuClasse = Menu(menubar, tearoff=0)
classeForm = ClasseForm(root)
menuClasse.add_command(label="Liste d'élèves par classe",
                       command=classeForm.form_display_byclasse)
menubar.add_cascade(label="Classe", menu=menuClasse)

# TODO : Option Set des classes et des élèves
# TODO : Menu des fonctionnalités Eleves, Classe, Matiere, Cours, Enseignant

# Emplacement des boutons de filtres
containerTOP = Frame(root, width=width, height=height / 5)

containerTOP.pack(side=TOP, fill=BOTH)

# Emplacement du calendrier
edt = AffichageEmploiDuTemps(root, width, height)
edt.currentdate = datetime.now().date()
edt.pack(side=TOP, fill=BOTH)

entrys = {
    "Classe": None
}

container = Frame(containerTOP)
listeOptions = SqliteService.getInstance().selectByQueryEntity(
    "SELECT libelleClasse FROM CLASSE")
listeOptions = ToolsBox.convert_rowlist_tostringlist(listeOptions)
optionClasse = OptionMenuCustom(container, listeOptions, entrys, "Classe")
container.pack(side=LEFT, fill=BOTH)

Label(containerTOP, text="Veuillez saisir une date pour afficher l'EDT : ").pack(side=LEFT)

container = Frame(containerTOP)
Label(container, text="Jour").pack(side=LEFT)
sb = Spinbox(container, from_=1, to=31, width=7, state="readonly")
sb.pack(side=LEFT)
entrys["Jour"] = sb
container.pack(side=LEFT, fill=BOTH)

container = Frame(containerTOP)
Label(container, text="Mois").pack(side=LEFT)
sb = Spinbox(container, from_=1, to=12, width=7, state="readonly")
sb.pack(side=LEFT)
entrys["Mois"] = sb
container.pack(side=LEFT, fill=BOTH)

container = Frame(containerTOP)
Label(container, text="Année").pack(side=LEFT)
sb = Spinbox(container, from_=2019, to=2022, width=7, state="readonly")
sb.pack(side=LEFT)
entrys["Annee"] = sb
container.pack(side=LEFT, fill=BOTH)

lbl = Label(containerTOP, text="")
lbl.pack(side=RIGHT)

edt.refreshLabelSemaineAfficher(lbl)

btnValider = Button(containerTOP, text="Valider la date", command=partial(
    edt.selectSemaineByDate, entrys=entrys, label=lbl)).pack(side=LEFT)


listCoursBySemaine = edt.controller.selectCours(
    edt.currentdate, entrys["Classe"].get())
edt.setCoursForSemaine(listCoursBySemaine, edt.currentdate)

optionClasse.v.trace("w", partial(edt.refreshCoursComponent, entrys=entrys))

# Emplacement des boutons suivant et précedent
containerBottom = Frame(root, bg='white', width=width, height=height / 5)
btnPrevious = Button(containerBottom, text="<", width=40, height=2, command=partial(
    edt.previousWeek, entrys=entrys, label=lbl)).pack(fill=X, side=LEFT)
btnNext = Button(containerBottom, text=">", width=40, height=2, command=partial(
    edt.nextWeek, entrys=entrys, label=lbl)).pack(fill=X, side=RIGHT)
containerBottom.pack(fill=BOTH, side=BOTTOM)

root.config(menu=menubar)
root.mainloop()
