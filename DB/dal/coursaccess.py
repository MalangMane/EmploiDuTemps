from tkinter import messagebox


def selectCoursForWeek(self, parameter_list):
    pass


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


def queryToUpdate(self):
    pass


def queryToGetMatiereAndEnseignant(self):
    pass


def queryToGetNomClasse(self):
    pass
