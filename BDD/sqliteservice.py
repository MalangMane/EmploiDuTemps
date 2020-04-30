from sqlite3 import *
from tkinter import messagebox

class SqliteService:
    instance = None
    def __init__(self):
        try:
            self.__conn = connect('tp3.db')
            self.__conn.row_factory = Row
            self.__curseur = self.__conn.cursor()
        except Error as e:
            messagebox.showerror("Erreur", e)

    
    @staticmethod
    def getInstance():
        if SqliteService.instance == None:
            SqliteService.instance = SqliteService()
            return SqliteService.instance
        else:
            return SqliteService.instance

    def insertByQuery(self,query):
        try:
            self.__curseur.execute(query)
            self.__conn.commit()
            messagebox.showinfo("Succès","L'import s'est déroulé avec succès")
        except Error as e:
            messagebox.showerror("Erreur", 'Erreur lors de l\'import de données : %s' % e.args)


    def insertEntity(self,tablename, datas):
        string = ''
        for data in datas[0]:
            string += '?,'
        string = string[:string.__len__() - 1]

        try:
            self.__curseur.executemany("INSERT INTO {0} VALUES ({1})".format(tablename,string),datas)
            self.__conn.commit()
            messagebox.showinfo("Succès","L'import s'est déroulé avec succès")
        except Error as e:
            messagebox.showerror("Erreur", 'Erreur lors de l\'import de données : %s' % e.args)


    def deleteEntity(self, tablename,idEntity):
        idName = tablename.lower().capitalize()
        if tablename.__contains__('APPRENANT'):
            idName = 'Eleve'
        try:
            champId = 'id{0}'.format(idName)
            self.__curseur.execute('DELETE FROM {0} WHERE {1} = {2}'.format(tablename,champId, idEntity))
            self.__conn.commit()
            messagebox.showinfo("Succès","La suppression s'est déroulé avec succès")
        except Error as e:
            messagebox.showerror("Erreur", 'Erreur lors de la suppression de données : %s' % e.args)

    def deleteEntityByQuery(self,query):
        try:
            self.__curseur.execute(query)
            self.__conn.commit()
            messagebox.showinfo("Succès","La suppression s'est déroulé avec succès")
        except Error as e:
            messagebox.showerror("Erreur", 'Erreur lors de la suppression de données : %s' % e.args)

    def updateEntity(self, query):
        try:
            self.__curseur.execute(query)
            self.__conn.commit()
            messagebox.showinfo("Succès","L'update s'est déroulé avec succès")
        except Error as e:
            messagebox.showerror("Erreur", 'Erreur lors de l\'update de données : %s' % e.args)



    def selectByQueryEntity(self,query):            
        try:
            return self.__curseur.execute(query).fetchall()
        except Error as e:
            print(e)
            messagebox.showerror("Erreur", 'Erreur lors de la récupération de données : %s' % e.args)


    def selectAllFieldEntity(self, tableName):
        query = 'SELECT * FROM %s' % tableName
        try:
            return self.__curseur.execute(query).fetchall()
        except Error as e:
            messagebox.showerror("Erreur", 'Erreur lors de la récupération de données : %s' % e.args)


    def close(self):
        self.__conn.close()
