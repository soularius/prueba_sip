from gluon import *
from gluon.sqlhtml import OptionsWidget
from gluon.sqlhtml import DateWidget

class Attendance:    
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'attendance' not in self.db.tables:
            self.db.define_table('attendance',
                            Field('classes_students_id', 'reference classes_students', ondelete='CASCADE'),
                            Field('date_class', 'date'),
                            Field('status', 'integer'),
                            Field('note', 'text'))
            
            # Validation for 'attendance'
            self.db.attendance.classes_students_id.requires = IS_IN_DB(self.db, self.db.classes_students.id, self.format_classes_students)

            status_options = [("1", "✔️"), ("0", "❌")]
            self.db.attendance.status.requires = IS_IN_SET(status_options, zero=None)
            self.db.attendance.date_class.requires = [IS_NOT_EMPTY(), IS_DATE()]

            self.db.attendance.classes_students_id.represent = lambda value, row: self.format_classes_students(value)
            self.db.attendance.status.represent = lambda value, row: "✔️" if value == 1 else "❌"

            self.db.attendance.classes_students_id.widget = OptionsWidget.widget
            self.db.attendance.date_class.widget = DateWidget.widget

            self.db.attendance.status.widget = SQLFORM.widgets.options.widget

            self.db.attendance.date_class.label = 'Fecha de asistencia'
            self.db.attendance.status.label = 'Estatus de asistencia'
            self.db.attendance.classes_students_id.label = 'Sección | Estudiante'
            self.db.attendance.note.label = 'Nota'

    def format_classes_students(self, value):
        # Retorna la representación de la relación clase-estudiante
        classes_students_record = self.db.classes_students(value.id)
        if classes_students_record:
            class_record = self.db.classes(classes_students_record.classes_id)
            student_record = self.db.students(classes_students_record.student_id)
            if class_record and student_record:
                class_code = class_record.code
                student_name = f"{student_record.name} {student_record.lastname}"
                return f"{class_code} | {student_name}"
        return "N/A"