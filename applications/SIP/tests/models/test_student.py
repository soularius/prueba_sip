import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.student import Student

class TestStudentModel(unittest.TestCase):
    def setUp(self):
        """
        Set up the initial configuration.

        This function initializes the `db` attribute with an instance of the DAL class, using a SQLite database in memory.
        It then defines a table named "Student" using the `define_table()` method of the Student class.
        Finally, it sets the `db` attribute of the current object to the initialized `db` attribute.

        Parameters:
            self: The current object.

        Returns:
            None
        """
        # Initial setup
        self.db = DAL('sqlite:memory:')
        Student(self.db).define_table()
        current.db = self.db

    def test_validation(self):
        """
        Test the validation of creating a record without required fields.

        This function tries to create a record without the required fields by calling the
        `insert()` method on the `self.db.students` object. It then attempts to commit the 
        changes to the database. If an exception is raised during the insertion or commit, 
        the database is rolled back to its previous state.

        After the insertion attempt, the function checks that no record has been created in 
        the `self.db.students` table by asserting that the count of records is 0.

        This function does not have any parameters or return types.
        """
        # Trying to create a record without required fields
        try:
            self.db.students.insert()
            self.db.commit()
        except:
            self.db.rollback()

        # Check that the record has not been created
        self.assertEqual(self.db(self.db.students).count(), 0)

    def test_update_student(self):
        """
        Update a student in the database.

        Args:
            self: The current instance of the class.
        
        Returns:
            None.
        """
        # Update a student
        student_id = self.db.students.insert(name="John", lastname="Doe", phone="1234567890", email="john@example.com")
        self.db(self.db.students.id == student_id).update(name="Jane")
        updated_student = self.db.students(student_id)

        # Validate the update
        self.assertEqual(updated_student.name, "Jane")

    def test_delete_student(self):
        """
        Test the functionality to delete a student.

        This function tests the ability to delete a student from the database. It first inserts a new student with the name "John", lastname "Doe", phone "1234567890", and email "john@example.com". Then it deletes the student using the student_id. Finally, it checks if the student has been successfully deleted by retrieving the student using the student_id and asserting that the retrieved student is None.

        Parameters:
        - self: The instance of the test class.

        Return:
        - None
        """
        # Delete a student
        student_id = self.db.students.insert(name="John", lastname="Doe", phone="1234567890", email="john@example.com")
        self.db(self.db.students.id == student_id).delete()
        deleted_student = self.db.students(student_id)

        # Validate the deletion
        self.assertIsNone(deleted_student)

    def tearDown(self):
        """
        Clean the environment after each test.
        """
        #Clean the environment after each test
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
