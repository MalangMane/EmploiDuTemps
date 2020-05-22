def insertTeacher(self, datas):
    self.sqlservice.insertEntity(
        tablename=self.TABLENAME_ENSEIGNANT, datas=datas)


def getTeacherIdWithName(self, firstname, lastname):
    query = """SELECT idEnseignant
                   FROM ENSEIGNANT
                   WHERE prenomEnseignant = '{0}' AND nomEnseignant = '{1}'""".format(firstname, lastname)
    return self.sqlservice.selectByQueryEntity(query=query)


def deleteTeacher(self, idTeacher):
    self.sqlservice.deleteEntity(
        tablename=self.TABLENAME_ENSEIGNANT, idEntity=idTeacher)


def deleteAssociationTeacherSubjectWithTeacherId(self, idTeacher):
    query = "DELETE FROM MATIERE_ENSEIGNANT WHERE k_idEnseignant = {0}".format(
        idTeacher)
    self.sqlservice.deleteEntityByQuery(query)


def insertSubjectAndTeacher(self, datas):
    self.sqlservice.insertEntity(self.TABLENAME_MATIERE_ENSEIGNANT, datas)
