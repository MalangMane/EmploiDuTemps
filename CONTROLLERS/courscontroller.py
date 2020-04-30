from BDD.sqliteservice import *
from datetime import *
import re

class CoursController:

    def __init__(self):
        self.TABLENAME = "COURS"
        self.sqlservice = SqliteService.getInstance()


    def checkingCours(self, entrys,prenomNomEnseignant):
        queryToCheckCoursIsDispo = """
            SELECT COUNT(crs.idCours) AS countCours
            FROM COURS AS crs
            INNER JOIN CLASSE AS cls ON crs.k_idClasse = cls.idClasse
            WHERE cls.libelleClasse = '{0}' AND crs.heureCours = '{1}' AND crs.jourCours = '{2}'
        """.format(entrys["Classe"].get() , entrys["Heure"].get() , entrys["Jour"].get())

        if self.sqlservice.selectByQueryEntity(queryToCheckCoursIsDispo)[0]['countCours'] != 0:
            messagebox.showerror("Indisponible", "Un cours a déjà lieu à ce créneau horaire")
            return False

        queryToCheckEnseignantIsDispo = """
            SELECT COUNT(crs.idCours) AS countCours
            FROM COURS AS crs
            INNER JOIN ENSEIGNANT AS e ON crs.k_idEnseignant = e.idEnseignant
            WHERE e.prenomEnseignant = '{0}' AND e.nomEnseignant = '{1}' AND crs.jourCours = '{2}' AND crs.heureCours = '{3}'
        """.format(prenomNomEnseignant[0] , prenomNomEnseignant[1] , entrys["Jour"].get(), entrys["Heure"].get())

        if self.sqlservice.selectByQueryEntity(queryToCheckEnseignantIsDispo)[0]['countCours'] != 0:
            messagebox.showerror("Indisponible", "Un cours a déjà lieu avec cette enseignant")
            return False

        return True



    def deleteCours(self,entrys):
        idCours = entrys["Jour/Heure/Matiere"].get().split()[0]
        self.sqlservice.deleteEntity(self.TABLENAME, idCours)


    def updateCours(self,entrys):
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

        

    def addCours(self,entrys):
        prenomNomEnseignant = entrys["Enseignant"].get().split()
        
        dateCours = ("{0}-{1}-{2}").format(entrys["Jour"].get(),entrys["Mois"].get(),entrys["Annee"].get())
        if self.checkingCours(entrys, prenomNomEnseignant) == False :return

        queryToGetMatiereAndEnseignant = """
            SELECT m_e.k_idMatiere , m_e.k_idEnseignant
            FROM MATIERE_ENSEIGNANT AS m_e
            INNER JOIN ENSEIGNANT AS e ON m_e.k_idEnseignant = e.idEnseignant
            INNER JOIN MATIERE AS mat ON m_e.k_idMatiere = mat.idMatiere
            WHERE e.nomEnseignant = '{0}' AND e.prenomEnseignant = '{1}' AND mat.libelleMatiere = '{2}' 
        """ .format(prenomNomEnseignant[1],prenomNomEnseignant[0],entrys["Matiere"].get())
        
        matiereEtEnseignant = self.sqlservice.selectByQueryEntity(query=queryToGetMatiereAndEnseignant)

        queryToGetNomClasse = """SELECT idClasse
                                 FROM CLASSE
                                 WHERE libelleClasse = '{0}'""".format(entrys["Classe"].get())

        laClasse = self.sqlservice.selectByQueryEntity(queryToGetNomClasse)

        datas = [(None,dateCours,entrys["Heure"].get(),laClasse[0]["idClasse"],matiereEtEnseignant[0]["k_idEnseignant"],matiereEtEnseignant[0]["k_idMatiere"])]

        self.sqlservice.insertEntity('COURS', datas)
    
    def selectCours(self, dateRef, classe):
        jourDeLaSemaine = dateRef.weekday()
        startDate = dateRef - timedelta(days=jourDeLaSemaine)
        result = []
        jour = (startDate).strftime("%d-%m-%Y")
        for i in range(7):
            query = """SELECT cls.libelleClasse, crs.jourCours, crs.heureCours, m.libelleMatiere, e.nomEnseignant, e.prenomEnseignant
                        FROM COURS AS crs
                        INNER JOIN MATIERE AS m ON crs.k_idMatiere =  m.idMatiere 
                        INNER JOIN ENSEIGNANT AS e  ON crs.k_idEnseignant = e.idEnseignant
                        INNER JOIN CLASSE  AS cls ON crs.k_idClasse = cls.idClasse
                        WHERE  crs.jourCours = \'{0}\' AND cls.libelleClasse = \'{1}\'""".format(jour , classe)
            result.append(self.sqlservice.selectByQueryEntity(query=query))
            jour = (startDate + timedelta(days=i)).strftime("%d-%m-%Y")
        return result
