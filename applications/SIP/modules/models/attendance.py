from gluon import *
from gluon.sqlhtml import OptionsWidget
from gluon.sqlhtml import DateWidget

class Attendance:    
    def __init__(self, db):
        self.db = db
    def define_table(self):
        """
        Define the 'attendance' table in the database.
        
        This function defines the 'attendance' table in the database if it does not already exist. The table has the following fields:
        
        - classes_students_id: A reference to the 'classes_students' table, representing the ID of the class and student combination. This field has a 'CASCADE' ondelete behavior.
        - date_class: The date of the class.
        - status: An integer representing the attendance status. It can be either 1 (for present) or 0 (for absent).
        - note: A text field for any additional notes.
        
        The function also sets up various validations, representations, and widgets for the 'attendance' table fields. It sets up the following validations:
        
        - classes_students_id.requires: The 'classes_students_id' field requires a value that exists in the 'classes_students' table, specifically in the 'section_class' column.
        - status.requires: The 'status' field requires a value that exists in a predefined set of options, represented by the 'status_options' list.
        - date_class.requires: The 'date_class' field requires a non-empty value and a valid date.
        
        The function also sets up the following representations for some fields:
        
        - classes_students_id.represent: The 'classes_students_id' field is represented by the section class value from the 'classes_students' table.
        - status.represent: The 'status' field is represented by a checkmark ('✔️') if the value is 1, and a cross mark ('❌') if the value is 0.
        
        The function also sets up the following widgets for some fields:
        
        - classes_students_id.widget: The 'classes_students_id' field uses the 'OptionsWidget' widget.
        - date_class.widget: The 'date_class' field uses the 'DateWidget' widget.
        - status.widget: The 'status' field uses the 'SQLFORM.widgets.options.widget'.
        
        The function also defines virtual fields for additional information:
        
        - student_name: A virtual field that retrieves the student name associated with the 'classes_students_id'.
        - salon_name: A virtual field that retrieves the salon name associated with the 'classes_students_id'.
        - subject_name: A virtual field that retrieves the subject name associated with the 'classes_students_id'.
        
        The function also sets labels for some fields:
        
        - date_class.label: The label for the 'date_class' field is set to 'Fecha de asistencia'.
        - status.label: The label for the 'status' field is set to 'Estatus de asistencia'.
        - classes_students_id.label: The label for the 'classes_students_id' field is set to 'Sección'.
        - student_name.label: The label for the 'student_name' field is set to 'Estudiante'.
        - salon_name.label: The label for the 'salon_name' field is set to 'Salon'.
        - subject_name.label: The label for the 'subject_name' field is set to 'Materia'.
        - note.label: The label for the 'note' field is set to 'Nota'.
        """
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
        """
        Formats the relationship between a class and a student.
        
        Parameters:
            value (int): The ID of the relationship between the class and student.
        
        Returns:
            str: The representation of the relationship between the class and student.
                 Returns "N/A" if the relationship does not exist.
        """
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
        """
        Retrieves the name of a student based on the given row.

        Parameters:
            row (Row): The row containing the attendance information.

        Returns:
            str: The name of the student if found in the database, otherwise "Desconocido".
                 If the classes_students_record is not found, returns "N/A".
        """
        classes_students_record = self.db.classes_students(row.attendance.classes_students_id)
        if classes_students_record:
            student_record = self.db.students(classes_students_record.student_id)
            return f"{student_record.name} {student_record.lastname}" if student_record else "Desconocido"
        return "N/A"

    def get_salon_name(self, row):
        """
        Retrieves the salon name associated with the given row.

        Parameters:
            row (Row): The row containing the attendance and classes_students_id.

        Returns:
            str: The name of the salon if found, "Desconocido" if not found, or "N/A" if the classes_students_record is not found.
        """
        classes_students_record = self.db.classes_students(row.attendance.classes_students_id)
        if classes_students_record:
            classes_record = self.db.classes(classes_students_record.classes_id)
            if classes_record:
                salons_record = self.db.salons(classes_record.salon_id)
                return f"{salons_record.name}" if salons_record else "Desconocido"
        return "N/A"

    def get_subject_name(self, row):
        """
        Returns the name of the subject associated with the given row.

        Parameters:
            row (Row): The row containing the attendance data.

        Returns:
            str: The name of the subject if it exists, otherwise "Desconocido".
        """
        classes_students_record = self.db.classes_students(row.attendance.classes_students_id)
        if classes_students_record:
            classes_record = self.db.classes(classes_students_record.classes_id)
            if classes_record:
                subject_record = self.db.subjects(classes_record.subject_id)
                return f"{subject_record.name}" if subject_record else "Desconocido"
        return "N/A"