from gluon import *
class ClassesStudents:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if not 'classes_students' in self.db.tables:
            self.db.define_table('classes_students',
                            Field('uuid', 'string', length=16, unique=True),
                            Field('class_uuid', 'reference classes'),
                            Field('student_uuid', 'reference students'))
            
            # Validation for 'classes_students'
            self.db.classes_students.class_uuid.requires = [IS_IN_DB(self.db, self.db.classes.uuid, '%(name)s')]
            self.db.classes_students.student_uuid.requires = [IS_IN_DB(self.db, self.db.students.uuid, '%(name)s')]