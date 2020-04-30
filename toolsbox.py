class ToolsBox():

    #fonction pour les optionMenu
    @staticmethod
    def convert_rowlist_tostringlist(rowlist):
        stringlist = []
        champ = rowlist[0].keys()[0]
        for row in rowlist:
            stringlist.append(row[champ])
        return stringlist
