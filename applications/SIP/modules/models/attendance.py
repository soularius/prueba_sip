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
            self.db.attendance.classes_students_id.requires = IS_IN_DB(self.db, self.db.classes_students.id, '%(section_class)s')

            status_options = [("1", "✔️"), ("0", "❌")]
            self.db.attendance.status.requires = IS_IN_SET(status_options, zero=None)
            self.db.attendance.date_class.requires = [IS_NOT_EMPTY(), IS_DATE()]

            self.db.attendance.classes_students_id.represent = lambda value, row: self.db.classes_students(value).section_class
            self.db.attendance.status.represent = lambda value, row: "✔️" if value == 1 else "❌"

            self.db.attendance.classes_students_id.widget = OptionsWidget.widget
            self.db.attendance.date_class.widget = DateWidget.widget

            self.db.attendance.status.widget = SQLFORM.widgets.options.widget

            self.db.attendance.student_name = Field.Virtual('student_name', lambda row: self.get_student_name(row))
            self.db.attendance.salon_name = Field.Virtual('salon_name', lambda row: self.get_salon_name(row))
            self.db.attendance.subject_name = Field.Virtual('subject_name', lambda row: self.get_subject_name(row))

            self.db.attendance.date_class.label = 'Fecha de asistencia'
            self.db.attendance.status.label = 'Estatus de asistencia'
            self.db.attendance.classes_students_id.label = 'Sección'
            self.db.attendance.student_name.label = 'Estudiante'
            self.db.attendance.salon_name.label = 'Salon'
            self.db.attendance.subject_name.label = 'Materia'
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
    
    def get_student_name(self, row):
        classes_students_record = self.db.classes_students(row.attendance.classes_students_id)
        if classes_students_record:
            student_record = self.db.students(classes_students_record.student_id)
            return f"{student_record.name} {student_record.lastname}" if student_record else "Desconocido"
        return "N/A"

    def get_salon_name(self, row):
        classes_students_record = self.db.classes_students(row.attendance.classes_students_id)
        if classes_students_record:
            classes_record = self.db.classes(classes_students_record.classes_id)
            if classes_record:
                salons_record = self.db.salons(classes_record.salon_id)
                return f"{salons_record.name}" if salons_record else "Desconocido"
        return "N/A"

    def get_subject_name(self, row):
        classes_students_record = self.db.classes_students(row.attendance.classes_students_id)
        if classes_students_record:
            classes_record = self.db.classes(classes_students_record.classes_id)
            if classes_record:
                subject_record = self.db.subjects(classes_record.subject_id)
                return f"{subject_record.name}" if subject_record else "Desconocido"
        return "N/A"