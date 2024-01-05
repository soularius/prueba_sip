from gluon import *
from gluon.sqlhtml import OptionsWidget

class ClassesStudents:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        """
        Define the 'classes_students' table if it doesn't exist in the database.

        This function creates the 'classes_students' table in the database if it is not already present. 
        The table has the following fields:
          - section_class: a string field with a maximum length of 45 characters. It should be unique.
          - classes_id: a foreign key field referencing the 'classes' table. On deletion of a record from 
            the 'classes' table, corresponding records in the 'classes_students' table will also be deleted.
          - student_id: a foreign key field referencing the 'students' table. On deletion of a record from 
            the 'students' table, corresponding records in the 'classes_students' table will also be deleted.

        The function also sets up the validation and representation of the fields in the 'classes_students' table:
          - section_class field requires a non-empty value.
          - classes_id field requires a value that exists in the 'classes' table.
          - student_id field requires a value that exists in the 'students' table.

        The representation of the 'classes_id' field is set to display the 'code' field of the referenced 
        record in the 'classes' table.
        The representation of the 'student_id' field is set to display the 'name' and 'lastname' fields 
        of the referenced record in the 'students' table.

        The widget for the 'classes_id' field is set to OptionsWidget.widget.
        The widget for the 'student_id' field is set to OptionsWidget.widget.

        The label for the 'classes_id' field is set to 'Codigo de la Clase'.
        The label for the 'student_id' field is set to 'Estudiante'.
        """
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