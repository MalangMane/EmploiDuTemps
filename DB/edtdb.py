from DB.sqliteservice import SqliteService


class EdtDb():
    def __init__(self, sqlservice):
        super().__init__()
        self.sqlservice = sqlservice

    from DB.dal.coursaccess import selectCoursForWeek, checkCoursIsDispo, checkEnseignantIsDispo
