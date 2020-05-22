from DB.edtdb import EdtDb
from DB.sqliteservice import SqliteService


class ClasseController:

    def __init__(self):
        self.edt_db = EdtDb(SqliteService.getInstance())

    def getElevesByClasse(self, entrys):
        return self.edt_db.getStudentForAClassSchool(entrys["Classe"].get())
