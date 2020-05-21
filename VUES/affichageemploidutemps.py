# TODO : créer une classe héritante de canvas pour l'espace de l'emploi du temps
from tkinter import *
from VUES.courscomponents import *
from CONTROLLERS.courscontroller import CoursController
from datetime import *


class AffichageEmploiDuTemps(Canvas):

    def __init__(self, master, width, height):
        self.courscomponents = []
        self.controller = CoursController()
        self.bg = '#ffcccc'
        self.width = width
        self.currentdate = ""
        self.height = (height) / 1.2
        super().__init__(master=master, width=self.width, height=self.height, bg=self.bg)

    def setCoursForSemaine(self, listCoursBySemaine, currentdate):
        self.currentdate = currentdate
        self.clearCoursComponents()
        if listCoursBySemaine.__len__() == 0:
            return
        for i in range(listCoursBySemaine.__len__()):
            for cours in listCoursBySemaine[i]:
                if listCoursBySemaine[i].__len__() == 0:
                    continue
                dayWeekToDisplay = datetime.strptime(
                    cours["jourCours"], "%d-%m-%Y").weekday() + 1
                if cours["heureCours"].__contains__("AM"):
                    self.courscomponents.append(CoursComponent(
                        canvas=self, jour=dayWeekToDisplay, heure=1, coursRow=cours))
                if cours["heureCours"].__contains__("PM"):
                    self.courscomponents.append(CoursComponent(
                        canvas=self, jour=dayWeekToDisplay, heure=2, coursRow=cours))
        print(len(self.courscomponents))

    def clearCoursComponents(self):
        for cours in self.courscomponents:
            cours.canvas.delete(cours.rectangle)
            cours.canvas.delete(cours.txtDescription)
        self.courscomponents = []

    def refreshCoursComponent(self, *args, entrys):
        listCoursBySemaine = self.controller.selectCours(
            self.currentdate, entrys["Classe"].get())
        self.setCoursForSemaine(listCoursBySemaine, self.currentdate)

    def nextWeek(self, entrys, label):
        derniereDateStocke = self.currentdate.strftime("%d-%m-%Y")
        date = datetime.strptime(
            derniereDateStocke, '%d-%m-%Y') + timedelta(days=7)
        listCoursBySemaine = self.controller.selectCours(
            date, entrys["Classe"].get())
        self.setCoursForSemaine(listCoursBySemaine, date)
        self.refreshLabelSemaineAfficher(label)

    def previousWeek(self, entrys, label):
        derniereDateStocke = self.currentdate.strftime("%d-%m-%Y")
        date = datetime.strptime(
            derniereDateStocke, '%d-%m-%Y') - timedelta(days=7)
        listCoursBySemaine = self.controller.selectCours(
            date, entrys["Classe"].get())
        self.setCoursForSemaine(listCoursBySemaine, date)
        self.refreshLabelSemaineAfficher(label)

    def selectSemaineByDate(self, entrys, label):
        dateSelect = "{0}-{1}-{2}".format(
            entrys["Jour"].get(), entrys["Mois"].get(), entrys["Annee"].get())
        dateSelect = datetime.strptime(dateSelect, '%d-%m-%Y')
        listCoursBySemaine = self.controller.selectCours(
            dateSelect, entrys["Classe"].get())
        self.setCoursForSemaine(listCoursBySemaine, dateSelect)
        self.refreshLabelSemaineAfficher(label)

    def refreshLabelSemaineAfficher(self, label):
        jourDeLaSemaine = self.currentdate.weekday()
        startDate = self.currentdate - timedelta(days=jourDeLaSemaine)
        endDate = startDate + timedelta(days=5)
        startDateString = (startDate).strftime("%d-%m-%Y")
        endDateString = (endDate).strftime("%d-%m-%Y")
        label["text"] = "Semaine actuelle : {0} au {1}".format(
            startDateString, endDateString)
