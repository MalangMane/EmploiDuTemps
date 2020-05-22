def insertStudent(self, data):
    self.sqlservice.insertEntity(tablename=self.TABLENAME_ELEVE, datas=data)


def deleteStudent(self, idStudent):
    self.sqlservice.deleteEntity(
        tablename=self.TABLENAME_ELEVE, idEntity=idStudent)


def selectStudentByNameAndClassSchool(self, firstname, lastname, classschoolName):
    query = """SELECT a.idEleve 
                   FROM APPRENANT AS a 
                   INNER JOIN CLASSE AS cls ON a.idClasse = cls.idClasse 
                   WHERE  a.nomApprenant = '{0}' AND a.prenomApprenant = '{1}' AND cls.libelleClasse = '{2}'""".format(
        lastname, firstname, classschoolName)
    return self.sqlservice.selectByQueryEntity(query=query)


def updateStudentWithClassSchool(self, classschoolName, firstname, lastname):
    query = '''UPDATE {0}
                    SET idClasse = (
                        SELECT idClasse 
                        FROM CLASSE 
                        WHERE libelleClasse = '{1}'
                    )
                    WHERE idEleve = (
                        SELECT idEleve 
                        FROM APPRENANT 
                        WHERE prenomApprenant = '{2}' AND nomApprenant = '{3}'
                    )'''.format(self.TABLENAME_ELEVE, classschoolName, firstname, lastname)
    self.sqlservice.updateEntity(query)


def getStudents(self):
    return self.sqlservice.selectAllFieldEntity(tablename=self.TABLENAME_ELEVE)
