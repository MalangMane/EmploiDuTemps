from BDD.sqliteservice import *
from tkinter import *

class EnseignantController:

    def __init__(self):
        self.sqlservice = SqliteService.getInstance()
        self.TABLENAME = 'ENSEIGNANT'

    def addEnseignant(self,entrys):
        datas = [(None,entrys["Nom"].get(),entrys["Prenom"].get())]
        self.sqlservice.insertEntity(tablename=self.TABLENAME, datas=datas)

    def deleteEnseignant(self,entrys):
        prenomNomEnseignant = entrys["Enseignant"].get().split()
        query = """SELECT idEnseignant FROM ENSEIGNANT WHERE prenomEnseignant = '{0}' AND nomEnseignant = '{1}'""".format(prenomNomEnseignant[0], prenomNomEnseignant[1])
        idEnseignant = self.sqlservice.selectByQueryEntity(query=query)[0]["idEnseignant"]
        self.sqlservice.deleteEntity(tablename=self.TABLENAME, idEntity=idEnseignant)
        self.sqlservice.deleteEntityByQuery("DELETE FROM MATIERE_ENSEIGNANT WHERE k_idEnseignant = {0}".format(idEnseignant))

    def associateEnseignantMatiere(self,entrys):
        nomPrenomEnseignant = entrys["Enseignant"].get().split()
        queryToGetIdMAtiere = """
            SELECT idMatiere 
            FROM MATIERE 
            WHERE libelleMatiere = '{0}'""".format(entrys["Matiere"].get())

        idMatiere = self.sqlservice.selectByQueryEntity(queryToGetIdMAtiere)[0]["idMatiere"]

        queryToGetIdEnseignant = """
            SELECT idEnseignant 
            FROM ENSEIGNANT 
            WHERE prenomEnseignant = '{0}' AND nomEnseignant = '{1}'
        """.format(nomPrenomEnseignant[0], nomPrenomEnseignant[1])

        idEnseignant = self.sqlservice.selectByQueryEntity(queryToGetIdEnseignant)[0]["idEnseignant"]

        datas = [(idEnseignant,idMatiere)]

        self.sqlservice.insertEntity('MATIERE_ENSEIGNANT', datas)