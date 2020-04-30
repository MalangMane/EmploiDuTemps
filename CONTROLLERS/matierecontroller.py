from BDD.sqliteservice import *
from tkinter import *

class MatiereController:

    def __init__(self):
        self.sqlservice = SqliteService.getInstance()
        self.TABLENAME = 'MATIERE'

    def addMatiere(self, entrys):
        datas = [(None,entrys["Matiere"].get())]
        self.sqlservice.insertEntity(tablename=self.TABLENAME, datas=datas)

    def deleteMatiere(self,entrys):
        query = """SELECT idMatiere FROM MATIERE WHERE libelleMatiere = '{0}'""".format(entrys["Matiere"].get())
        idMatiere = self.sqlservice.selectByQueryEntity(query=query)[0]["idMatiere"]
        self.sqlservice.deleteEntity(tablename=self.TABLENAME, idEntity=idMatiere)
        self.sqlservice.deleteEntityByQuery("DELETE FROM MATIERE_ENSEIGNANT WHERE k_idMatiere = {0}".format(idMatiere))