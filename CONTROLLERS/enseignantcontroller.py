from DB.sqliteservice import *
from DB.edtdb import EdtDb
from tkinter import *


class EnseignantController:

    def __init__(self):
        self.edt_db = EdtDb(SqliteService.getInstance())

    def addEnseignant(self, entrys):
        datas = [(None, entrys["Nom"].get(), entrys["Prenom"].get())]
        self.edt_db.insertTeacher(self.edt_db, datas)

    def deleteEnseignant(self, entrys):
        prenomNomEnseignant = entrys["Enseignant"].get().split()

        idTeacher = self.edt_db.getTeacherIdWithName(
            self.edt_db, prenomNomEnseignant[0], prenomNomEnseignant[1])

        if idTeacher.__len__() == 0:
            messagebox.showerror('Erreur', 'Enseignant introuvable')
            return
        idTeacher = idTeacher[0]["idEnseignant"]

        self.edt_db.deleteTeacher(self.edt_db, idTeacher)
        self.edt_db.deleteAssociationTeacherSubjectWithTeacherId(
            self.edt_db, idTeacher)

    def associateEnseignantMatiere(self, entrys):
        nomPrenomEnseignant = entrys["Enseignant"].get().split()
        idSubject = self.edt_db.getIdSubjectByName(
            self.edt_db, entrys["Matiere"].get())

        if idSubject.__len__() == 0:
            messagebox.showerror('Erreur', 'Matière introuvable')
            return

        idSubject = idSubject[0]["idMatiere"]
        idTeacher = self.edt_db.getTeacherIdWithName(
            self.edt_db, nomPrenomEnseignant[0], nomPrenomEnseignant[1])

        if idTeacher.__len__() == 0:
            messagebox.showerror('Erreur', 'Enseignant introuvable')
            return
        idTeacher = idTeacher[0]["idEnseignant"]
        datas = [(idTeacher, idSubject)]
        self.edt_db.insertSubjectAndTeacher(self.edt_db, datas)
