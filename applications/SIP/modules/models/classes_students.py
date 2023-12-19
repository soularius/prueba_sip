from gluon import *
class ClassesStudents:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'classes_students' not in self.db.tables:
            self.db.define_table('classes_students',
                                 Field('class_id', 'reference classes', ondelete='CASCADE'),
                                 Field('student_id', 'reference students', ondelete='CASCADE'))
            
            # Validation for 'classes_students'
            self.db.classes_students.class_id.requires = IS_IN_DB(self.db, self.db.classes.id, '%(name)s')
            self.db.classes_students.student_id.requires = IS_IN_DB(self.db, self.db.students.id, '%(name)s')
