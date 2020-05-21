from tkinter import *
from enum import Enum
from datetime import datetime


class CoursComponent():
    def __init__(self, canvas, jour, heure, coursRow):
        self.canvas = canvas
        print(coursRow["libelleMatiere"])
        print(coursRow["nomEnseignant"])
        self.width = int(self.canvas["width"]) / 6
        self.height = int(self.canvas["height"]) / 2
        self.posx = self.width * jour
        self.posy = self.height * heure
        self.rectangle = self.canvas.create_rectangle(
            self.posx - self.width, self.posy - self.height, self.posx, self.posy, fill='#80ffaa')
        self.txtDescription = self.canvas.create_text((self.posx - self.width) + (self.width / 2), (self.posy - self.height) + (
            self.height / 2), fill="black", text="Cours : {0} \nIntervenant : {1} {2}".format(coursRow["libelleMatiere"], coursRow["nomEnseignant"], coursRow["prenomEnseignant"]))
