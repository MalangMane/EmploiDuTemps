from DB.sqliteservice import *
from DB.edtdb import EdtDb
from tkinter import *


class MatiereController:

    def __init__(self):
        self.edt_db = EdtDb(SqliteService.getInstance())

    def addMatiere(self, entrys):
        datas = [(None, entrys["Matiere"].get())]
        self.edt_db.insertSubject(self.edt_db, datas)

    def deleteMatiere(self, entrys):
        idSubject = self.edt_db.getIdSubjectByName(
            self.edt_db, entrys["Matiere"].get())

        if idSubject.__len__() == 0:
            messagebox.showerror('Erreur', 'Matière introuvable')
            return

        idSubject = idSubject[0]["idMatiere"]

        self.edt_db.deleteSubject(self.edt_db, idSubject)
        self.edt_db.deleteAssociationTeacherSubjectWithSubjectId(
            self.edt_db, idSubject)
