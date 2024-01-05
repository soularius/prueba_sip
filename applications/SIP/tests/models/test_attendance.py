import unittest
from gluon.dal import DAL, Field
from gluon.validators import IS_IN_DB, IS_NOT_EMPTY, IS_DATE
from applications.SIP.modules.models.attendance import Attendance

class TestAttendanceModel(unittest.TestCase):
    
    def setUp(self):
        # Create a DAL instance for testing, using an in-memory SQLite database
        self.db = DAL('sqlite:memory:')
        
        # Define necessary tables and relations required for the Attendance model
        self.db.define_table('students',
                             Field('name', 'string'),
                             Field('lastname', 'string'))
        
        self.db.define_table('salons',
                             Field('name', 'string'))

        self.db.define_table('subjects',
                             Field('name', 'string'))

        self.db.define_table('classes',
                             Field('code', 'string'),
                             Field('salon_id', 'reference salons'),
                             Field('subject_id', 'reference subjects'))

        self.db.define_table('classes_students',
                             Field('classes_id', 'reference classes'),
                             Field('student_id', 'reference students'),
                             Field('section_class', 'string'))

        # Initialize the Attendance model
        self.attendance_model = Attendance(self.db)
        self.attendance_model.define_table()

    def test_table_definition(self):
        # Test if the 'attendance' table is defined
        self.assertIn('attendance', self.db.tables)

        # Test field properties
        self.assertTrue(isinstance(self.db.attendance.classes_students_id.requires, IS_IN_DB))
        self.assertTrue(isinstance(self.db.attendance.date_class.requires[0], IS_NOT_EMPTY))
        self.assertTrue(isinstance(self.db.attendance.date_class.requires[1], IS_DATE))

    def test_virtual_fields(self):
        # Test the virtual fields by creating a dummy record
        student_id = self.db.students.insert(name="John", lastname="Doe")
        salon_id = self.db.salons.insert(name="Salon A")
        subject_id = self.db.subjects.insert(name="Math")
        class_id = self.db.classes.insert(code="MATH101", salon_id=salon_id, subject_id=subject_id)
        classes_students_id = self.db.classes_students.insert(classes_id=class_id, student_id=student_id, section_class="A1")

        attendance_id = self.db.attendance.insert(classes_students_id=classes_students_id, date_class="2023-01-01", status=1)

        # Retrieve the created record
        attendance_record = self.db.attendance[attendance_id]

        # Test virtual fields
        self.assertEqual(attendance_record.student_name, "John Doe")
        self.assertEqual(attendance_record.salon_name, "Salon A")
        self.assertEqual(attendance_record.subject_name, "Math")

    def tearDown(self):
        # Clean up and drop tables after tests
        self.db.attendance.drop()
        self.db.classes_students.drop()
        self.db.classes.drop()
        self.db.subjects.drop()
        self.db.salons.drop()
        self.db.students.drop()
        self.db.close()

if __name__ == '__main__':
    unittest.main()
