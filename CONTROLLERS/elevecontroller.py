from DB.sqliteservice import SqliteService
from DB.edtdb import EdtDb
from tkinter import messagebox


class EleveController:

    def __init__(self):
        self.edt_db = EdtDb(SqliteService.getInstance())

    def addEleve(self, entrys):

        idClasse = self.edt_db.getClassSchoolId(
            self.edt_db, entrys["Classe"].get())

        if idClasse.__len__() == 0:
            messagebox.showerror('Indisponible', 'Aucune classe a été trouvé')
            return

        idClasse = idClasse[0]["idClasse"]
        datas = [(entrys["Nom"].get(), entrys["Prenom"].get(), None, idClasse)]
        self.edt_db.insertStudent(self.edt_db, datas)

    def deleteEleve(self, entrys):
        nomprenom = entrys["Eleves"].get().split()
        idStudent = self.edt_db.selectStudentByNameAndClassSchool(
            self.edt_db, nomprenom[1], nomprenom[0], entrys["Classe"].get())

        if idStudent.__len__() == 0:
            messagebox.showerror('Erreur', 'Aucun élève a été trouvé')
            return

        self.edt_db.deleteStudent(self.edt_db, idStudent[0]["idEleve"])

    def associateEleveWithClasse(self, entrys):
        nomprenom = entrys["Eleves"].get().split()
        self.edt_db.updateStudentWithClassSchool(
            self.edt_db, entrys["NewClasse"].get(), nomprenom[0], nomprenom[1])

    def getEleves(self):
        return self.edt_db.getStudents(self.edt_db)
