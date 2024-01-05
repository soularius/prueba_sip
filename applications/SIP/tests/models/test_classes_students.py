import unittest
from gluon.dal import DAL, Field
from gluon.validators import IS_NOT_EMPTY, IS_IN_DB
from applications.SIP.modules.models.classes_students import ClassesStudents

class TestClassesStudentsModel(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test environment for testing the ClassesStudents model.

        This function creates a DAL instance for testing, using an in-memory SQLite database. It then defines the 'students' table with 'name' and 'lastname' fields, and the 'classes' table with a 'code' field. Finally, it initializes the ClassesStudents model and defines its table.

        Parameters:
            self (object): The instance of the test class.

        Returns:
            None
        """
        # Create a DAL instance for testing, using an in-memory SQLite database
        self.db = DAL('sqlite:memory:')
        
        # Define necessary tables and relations required for the ClassesStudents model
        self.db.define_table('students',
                             Field('name', 'string'),
                             Field('lastname', 'string'))
        
        self.db.define_table('classes',
                             Field('code', 'string'))

        # Initialize the ClassesStudents model
        self.classes_students_model = ClassesStudents(self.db)
        self.classes_students_model.define_table()

    def test_table_definition(self):
        """
        Test if the 'classes_students' table is defined.
        """
        # Test if the 'classes_students' table is defined
        self.assertIn('classes_students', self.db.tables)

        # Test field properties
        self.assertTrue(isinstance(self.db.classes_students.section_class.requires, IS_NOT_EMPTY))
        self.assertTrue(isinstance(self.db.classes_students.classes_id.requires, IS_IN_DB))
        self.assertTrue(isinstance(self.db.classes_students.student_id.requires, IS_IN_DB))

    def test_field_representations(self):
        """
        Test the field representations for the given dummy records.

        This function creates dummy records for testing the field representations
        of the 'classes_students' table. It inserts a dummy student, class, and
        classes_students record into the database. Then it retrieves the created
        record as a Rows object and tests the field representations of the
        'classes_id' and 'student_id' fields. It asserts that the representations
        match the expected values.

        Parameters:
        - self: The current instance of the test class.

        Returns:
        - None
        """
        # Create dummy records for testing field representations
        student_id = self.db.students.insert(name="John", lastname="Doe")
        class_id = self.db.classes.insert(code="MATH101")
        classes_students_id = self.db.classes_students.insert(section_class="A1", classes_id=class_id, student_id=student_id)

        # Retrieve the created record as a Rows object
        classes_students_record = self.db(self.db.classes_students.id == classes_students_id).select().first()

        # Test field representations
        self.assertEqual(self.db.classes_students.classes_id.represent(classes_students_record.classes_id, classes_students_record), "MATH101")
        self.assertEqual(self.db.classes_students.student_id.represent(classes_students_record.student_id, classes_students_record), "John Doe")


    def tearDown(self):
        """
        Clean up and drop tables after tests
        """
        # Clean up and drop tables after tests
        self.db.classes_students.drop()
        self.db.classes.drop()
        self.db.students.drop()
        self.db.close()

if __name__ == '__main__':
    unittest.main()
