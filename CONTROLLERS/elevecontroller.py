from BDD.sqliteservice import *
from tkinter import *
class EleveController:

    def __init__(self):
        self.sqlservice = SqliteService.getInstance()
        self.TABLENAME = 'APPRENANT'


    def addEleve(self,entrys):
        query = """SELECT idClasse
                    FROM CLASSE
                    WHERE libelleClasse = \"%s\"""" % entrys["Classe"].get() 
        idClasse = self.sqlservice.selectByQueryEntity(query=query)[0]["idClasse"]
        datas = [(entrys["Nom"].get() ,entrys["Prenom"].get() ,None,idClasse)]
        self.sqlservice.insertEntity(tablename=self.TABLENAME, datas=datas)


    def deleteEleve(self,entrys):
        nomprenom = entrys["Eleves"].get().split()
        query = """SELECT a.idEleve FROM APPRENANT AS a INNER JOIN CLASSE AS cls ON a.idClasse = cls.idClasse WHERE  a.nomApprenant = '{0}' AND a.prenomApprenant = '{1}' AND cls.libelleClasse = '{2}'""".format(nomprenom[1], nomprenom[0], entrys["Classe"].get() )
        idEleve = self.sqlservice.selectByQueryEntity(query=query)[0]["idEleve"]
        self.sqlservice.deleteEntity(tablename=self.TABLENAME, idEntity=idEleve)
            

    def associateEleveWithClasse(self,entrys):
        nomprenom = entrys["Eleves"].get().split()
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
                    )'''.format(self.TABLENAME,entrys["NewClasse"].get() ,nomprenom[0], nomprenom[1])
        self.sqlservice.updateEntity(query)

    def getEleves(self):
        return self.sqlservice.selectAllFieldEntity(tablename=self.TABLENAME)