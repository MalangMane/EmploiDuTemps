from tkinter import messagebox
from _datetime import timedelta


def selectCoursForWeek(self, day, classschoolName, startDate):
    result = []
    for i in range(1, 7):
        query = """SELECT cls.libelleClasse, crs.jourCours, crs.heureCours, m.libelleMatiere, e.nomEnseignant, e.prenomEnseignant
                        FROM COURS AS crs
                        INNER JOIN MATIERE AS m ON crs.k_idMatiere =  m.idMatiere
                        INNER JOIN ENSEIGNANT AS e  ON crs.k_idEnseignant = e.idEnseignant
                        INNER JOIN CLASSE  AS cls ON crs.k_idClasse = cls.idClasse
                        WHERE  crs.jourCours = \'{0}\' AND cls.libelleClasse = \'{1}\'""".format(day, classschoolName)
        cours = self.sqlservice.selectByQueryEntity(query=query)
        if cours.__len__() != 0:
            result.append(cours)
        day = (startDate + timedelta(days=i)).strftime("%d-%m-%Y")

    return result


def insertCourse(self, data):
    self.sqlservice.insertEntity(self.TABLENAME_COURS, data)


def deleteCourse(self, idCourse):
    self.sqlservice.deleteEntity(self.TABLENAME_COURS, idCourse)


def checkCoursIsDispo(self, classschool, hour, day):
    checkCoursIsDispo = """
            SELECT COUNT(crs.idCours) AS countCours
            FROM COURS AS crs
            INNER JOIN CLASSE AS cls ON crs.k_idClasse = cls.idClasse
            WHERE cls.libelleClasse = '{0}' AND crs.heureCours = '{1}' AND crs.jourCours = '{2}'
        """.format(classschool, hour, day)

    if self.sqlservice.selectByQueryEntity(checkCoursIsDispo)[0]['countCours'] != 0:
        messagebox.showerror(
            "Indisponible", "Un cours a déjà lieu à ce créneau horaire")
        return False
    return True


def checkEnseignantIsDispo(self, firstname, lastname, date, hour):
    queryToCheckEnseignantIsDispo = """
            SELECT COUNT(crs.idCours) AS countCours
            FROM COURS AS crs
            INNER JOIN ENSEIGNANT AS e ON crs.k_idEnseignant = e.idEnseignant
            WHERE e.prenomEnseignant = '{0}' AND e.nomEnseignant = '{1}' AND crs.jourCours = '{2}' AND crs.heureCours = '{3}'
        """.format(firstname, lastname, date, hour)

    if self.sqlservice.selectByQueryEntity(queryToCheckEnseignantIsDispo)[0]['countCours'] != 0:
        messagebox.showerror(
            "Indisponible", "Un cours a déjà lieu avec cette enseignant")
        return False

    return True


def updateCourse(self, tableName, classschool, lastname, firstname, subjectName, idCours):
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
    """.format(tableName, classschool, lastname, firstname, subjectName, idCours)
    self.sqlservice.updateEntity(queryToUpdate)


def getIdSubjectAndIdTeacher(self, firstname, lastname, classschool):
    queryToGetMatiereAndEnseignant = """
            SELECT m_e.k_idMatiere , m_e.k_idEnseignant
            FROM MATIERE_ENSEIGNANT AS m_e
            INNER JOIN ENSEIGNANT AS e ON m_e.k_idEnseignant = e.idEnseignant
            INNER JOIN MATIERE AS mat ON m_e.k_idMatiere = mat.idMatiere
            WHERE e.nomEnseignant = '{0}' AND e.prenomEnseignant = '{1}' AND mat.libelleMatiere = '{2}' 
    """ .format(lastname, firstname, classschool)

    return self.sqlservice.selectByQueryEntity(
        query=queryToGetMatiereAndEnseignant)


def getClassSchoolId(self, classschoolName):
    queryToGetNomClasse = """SELECT idClasse
                                 FROM CLASSE
                                 WHERE libelleClasse = '{0}'""".format(classschoolName)
    return self.sqlservice.selectByQueryEntity(queryToGetNomClasse)
