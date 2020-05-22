def getStudentForAClassSchool(self, classschoolName):
    query = """SELECT a.nomApprenant , a.prenomApprenant
                    FROM APPRENANT AS a
                    INNER JOIN CLASSE as c ON a.idClasse = c.idClasse
                    WHERE c.libelleClasse = '{0}'""".format(classschoolName)
    return self.sqlservice.selectEntity(query=query)
