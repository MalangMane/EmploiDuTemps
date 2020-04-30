from BDD.sqliteservice import *

class ClasseController:

    def __init__(self):
        self.TABLENAME = "CLASSE"
        self.sqlservice = SqliteService.getInstance()

    def getElevesByClasse(self, entrys):
        query = """SELECT a.nomApprenant , a.prenomApprenant
                    FROM APPRENANT AS a
                    INNER JOIN CLASSE as c ON a.idClasse = c.idClasse
                    WHERE c.libelleClasse = '{0}'""".format(entrys["Classe"].get())
        return self.sqlservice.selectEntity(query=query)