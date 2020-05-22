from DB.sqliteservice import SqliteService


class EdtDb():
    def __init__(self, sqlservice):
        super().__init__()
        self.sqlservice = sqlservice
        self.TABLENAME_COURS = 'COURS'
        self.TABLENAME_MATIERE = 'MATIERE'
        self.TABLENAME_CLASSE = 'CLASSE'
        self.TABLENAME_ELEVE = 'ELEVE'
        self.TABLENAME_ENSEIGNANT = 'ENSEIGNANT'
        self.TABLENAME_MATIERE_ENSEIGNANT = 'MATIERE_ENSEIGNANT'

    from DB.dal.coursaccess import selectCoursForWeek, checkCoursIsDispo, checkEnseignantIsDispo, updateCourse, insertCourse, getClassSchoolId, getIdSubjectAndIdTeacher, deleteCourse
    from DB.dal.classeaccess import getStudentForAClassSchool
    from DB.dal.eleveaccess import insertStudent, deleteStudent, selectStudentByNameAndClassSchool, updateStudentWithClassSchool, getStudents
    from DB.dal.enseignantaccess import insertTeacher, getTeacherIdWithName, deleteAssociationTeacherSubjectWithTeacherId, deleteTeacher, insertSubjectAndTeacher
    from DB.dal.matiereaccess import getIdSubjectByName, insertSubject, deleteAssociationTeacherSubjectWithSubjectId, deleteSubject
