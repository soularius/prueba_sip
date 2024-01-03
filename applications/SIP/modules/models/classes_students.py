from gluon import *
from gluon.sqlhtml import OptionsWidget

class ClassesStudents:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'classes_students' not in self.db.tables:
            self.db.define_table('classes_students',
                                 Field('section_class', 'string', length=45, unique=True),
                                 Field('classes_id', 'reference classes', ondelete='CASCADE'),
                                 Field('student_id', 'reference students', ondelete='CASCADE'))
            
            # Validation for 'classes_students'
            self.db.classes_students.section_class.requires = IS_NOT_EMPTY()
            self.db.classes_students.classes_id.requires = IS_IN_DB(self.db, self.db.classes.id, '%(code)s')
            self.db.classes_students.student_id.requires = IS_IN_DB(self.db, self.db.students.id, '%(name)s %(lastname)s')

            self.db.classes_students.classes_id.represent = lambda value, row: self.db.classes(value).code
            self.db.classes_students.student_id.represent = lambda value, row: f"{self.db.students(value).name} {self.db.students(value).lastname}"

            self.db.classes_students.classes_id.widget = OptionsWidget.widget
            self.db.classes_students.student_id.widget = OptionsWidget.widget

            self.db.classes_students.classes_id.label = 'Codigo de la Clase'
            self.db.classes_students.student_id.label = 'Estudiante'