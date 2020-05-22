from DB.sqliteservice import *
from DB.edtdb import EdtDb
from datetime import *
import re


class CoursController:

    def __init__(self):
        self.edt_db = EdtDb(SqliteService.getInstance())

    def checkingCours(self, entrys, prenomNomEnseignant):
        if self.edt_db.checkCoursIsDispo(self.edt_db, entrys["Classe"].get(), entrys["Heure"].get(), entrys["Jour"].get()) == False:
            return False

        if self.edt_db.checkEnseignantIsDispo(self.edt_db, prenomNomEnseignant[0], prenomNomEnseignant[1], entrys["Jour"].get(), entrys["Heure"].get()) == False:
            return False

        return True

    def deleteCours(self, entrys):
        idCourse = entrys["Jour/Heure/Matiere"].get().split()[0]
        self.edt_db.deleteCourse(self.edt_db, idCourse)

    def updateCours(self, entrys):
        prenomNomEnseignant = entrys["Enseignant"].get().split()
        idCours = entrys["Jour/Heure/Matiere"].get().split()[0]
        self.edt_db.updateCourse(self.edt_db, self.TABLENAME, entrys["Classe"].get(
        ), prenomNomEnseignant[1], prenomNomEnseignant[0], entrys["Matiere"].get(), idCours)

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

        matiereEtEnseignant = self.edt_db.getIdSubjectAndIdTeacher(
            self.edt_db, prenomNomEnseignant[1], prenomNomEnseignant[0], entrys["Matiere"].get())

        laClasse = self.edt_db.getClassSchoolId(
            self.edt_db, entrys["Classe"].get())

        datas = [(None, dateCours, entrys["Heure"].get(), laClasse[0]["idClasse"],
                  matiereEtEnseignant[0]["k_idEnseignant"], matiereEtEnseignant[0]["k_idMatiere"])]

        self.edt_db.insertCours(self.edt_db, data=datas)

    def selectCours(self, dateRef, classschool):
        dayOfWeek = dateRef.weekday()
        startDate = dateRef - timedelta(days=dayOfWeek)
        result = []
        day = (startDate).strftime("%d-%m-%Y")
        return self.edt_db.selectCoursForWeek(self.edt_db, day, classschool, startDate)
