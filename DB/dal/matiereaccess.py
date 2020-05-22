def getIdSubjectByName(self, subjectName):
    queryToGetIdMAtiere = """
            SELECT idMatiere 
            FROM MATIERE 
            WHERE libelleMatiere = '{0}'""".format(subjectName)

    return self.sqlservice.selectByQueryEntity(queryToGetIdMAtiere)


def insertSubject(self, datas):
    self.sqlservice.insertEntity(tablename=self.TABLENAME_MATIERE, datas=datas)


def deleteAssociationTeacherSubjectWithSubjectId(self, idSubject):
    self.sqlservice.deleteEntityByQuery(
        "DELETE FROM MATIERE_ENSEIGNANT WHERE k_idMatiere = {0}".format(idSubject))


def deleteSubject(self, idSubject):
    self.sqlservice.deleteEntity(
        tablename=self.TABLENAME_MATIERE, idEntity=idSubject)
