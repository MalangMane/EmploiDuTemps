from DB.sqliteservice import *
from DB.edtdb import EdtDb
from datetime import *
import re


class CoursController:

    def __init__(self):
        self.TABLENAME = "COURS"
        self.sqlservice = SqliteService.getInstance()
        self.edt_db = EdtDb(self.sqlservice)

    def checkingCours(self, entrys, prenomNomEnseignant):
        if self.edt_db.queryToCheckCoursIsDispo(self.edt_db, entrys["Classe"].get(), entrys["Heure"].get(), entrys["Jour"].get()) == False:
            return False

        if self.edt_db.queryToCheckEnseignantIsDispo(self.edt_db, prenomNomEnseignant[0], prenomNomEnseignant[1], entrys["Jour"].get(), entrys["Heure"].get()) == False:
            return False

        return True

    def deleteCours(self, entrys):
        idCours = entrys["Jour/Heure/Matiere"].get().split()[0]
        self.sqlservice.deleteEntity(self.TABLENAME, idCours)

    def updateCours(self, entrys):
        prenomNomEnseignant = entrys["Enseignant"].get().split()
        idCours = entrys["Jour/Heure/Matiere"].get().split()[0]

        queryToUpdate = """
            UPDATE {0}
            SET k_idClasse = (
                SELECT idClasse
                FROM CLASSE
                WHERE libelleClasse = '{1}'
            ),
            k_idEnseignant = (
                SELECT idEnseignant
                FROM ENSEIGNANT
                WHERE nomEnseignant = '{2}' AND prenomEnseignant = '{3}'
            ),
            k_idMatiere = (
                SELECT idMatiere
                FROM MATIERE
                WHERE libelleMatiere = '{4}'
            )
            WHERE idCours = {5}
        """.format(self.TABLENAME, entrys["Classe"].get(), prenomNomEnseignant[1], prenomNomEnseignant[0], entrys["Matiere"].get(), idCours)

        self.sqlservice.updateEntity(queryToUpdate)

    def addCours(self, entrys):
        prenomNomEnseignant = entrys["Enseignant"].get().split()

        mois = entrys["Mois"].get()
        if int(mois) < 10:
            mois = '0' + mois

        jours = entrys["Jour"].get()
        if int(jours) < 10:
            jours = '0' + jours

        dateCours = (
            "{0}-{1}-{2}").format(jours, mois, entrys["Annee"].get())
        if self.checkingCours(entrys, prenomNomEnseignant) == False:
            return

        queryToGetMatiereAndEnseignant = """
            SELECT m_e.k_idMatiere , m_e.k_idEnseignant
            FROM MATIERE_ENSEIGNANT AS m_e
            INNER JOIN ENSEIGNANT AS e ON m_e.k_idEnseignant = e.idEnseignant
            INNER JOIN MATIERE AS mat ON m_e.k_idMatiere = mat.idMatiere
            WHERE e.nomEnseignant = '{0}' AND e.prenomEnseignant = '{1}' AND mat.libelleMatiere = '{2}' 
        """ .format(prenomNomEnseignant[1], prenomNomEnseignant[0], entrys["Matiere"].get())

        matiereEtEnseignant = self.sqlservice.selectByQueryEntity(
            query=queryToGetMatiereAndEnseignant)

        queryToGetNomClasse = """SELECT idClasse
                                 FROM CLASSE
                                 WHERE libelleClasse = '{0}'""".format(entrys["Classe"].get())

        laClasse = self.sqlservice.selectByQueryEntity(queryToGetNomClasse)

        datas = [(None, dateCours, entrys["Heure"].get(), laClasse[0]["idClasse"],
                  matiereEtEnseignant[0]["k_idEnseignant"], matiereEtEnseignant[0]["k_idMatiere"])]

        self.sqlservice.insertEntity('COURS', datas)

    def selectCours(self, dateRef, classe):
        jourDeLaSemaine = dateRef.weekday()
        startDate = dateRef - timedelta(days=jourDeLaSemaine)
        result = []
        jour = (startDate).strftime("%d-%m-%Y")
        for i in range(1, 7):
            query = """SELECT cls.libelleClasse, crs.jourCours, crs.heureCours, m.libelleMatiere, e.nomEnseignant, e.prenomEnseignant
                        FROM COURS AS crs
                        INNER JOIN MATIERE AS m ON crs.k_idMatiere =  m.idMatiere 
                        INNER JOIN ENSEIGNANT AS e  ON crs.k_idEnseignant = e.idEnseignant
                        INNER JOIN CLASSE  AS cls ON crs.k_idClasse = cls.idClasse
                        WHERE  crs.jourCours = \'{0}\' AND cls.libelleClasse = \'{1}\'""".format(jour, classe)
            cours = self.sqlservice.selectByQueryEntity(query=query)
            if cours.__len__() != 0:
                result.append(cours)
            jour = (startDate + timedelta(days=i)).strftime("%d-%m-%Y")
        return result
