import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.teachers import Teachers

class TestTeachersModel(unittest.TestCase):
    def setUp(self):
        """
        Set up the initial configuration.
        """
        # Initial setup
        self.db = DAL('sqlite:memory:')
        Teachers(self.db).define_table()
        current.db = self.db

    def test_validation(self):
        """
        Test the validation of creating a record without the required fields.

        This function attempts to create a record without the required fields in the 
        'teachers' table. It then checks that the record was not created by verifying 
        the count of 'teachers' records in the database.

        Parameters:
            self (object): The current instance of the test class.

        Returns:
            None
        """
        # Trying to create a record without required fields
        try:
            self.db.teachers.insert()
            self.db.commit()
        except:
            self.db.rollback()

        # Check that the record has not been created
        self.assertEqual(self.db(self.db.teachers).count(), 0)

    def test_update_teacher(self):
        """
        Update a teacher.
        """
        # Update a teacher
        teacher_id = self.db.teachers.insert(name="Juan", lastname="Pérez", email="juan@example.com", phone="1234567890")
        self.db(self.db.teachers.id == teacher_id).update(name="Carlos")
        updated_teacher = self.db.teachers(teacher_id)

        # Validate the update
        self.assertEqual(updated_teacher.name, "Carlos")

    def test_delete_teacher(self):
        """
        Delete a teacher from the database.
        
        Args:
            self: The instance of the test class.
        
        Returns:
            None
        """
        # Delete a teacher
        teacher_id = self.db.teachers.insert(name="Juan", lastname="Pérez", email="juan@example.com", phone="1234567890")
        self.db(self.db.teachers.id == teacher_id).delete()
        deleted_teacher = self.db.teachers(teacher_id)

        # Validate the deletion
        self.assertIsNone(deleted_teacher)

    def tearDown(self):
        """
        Clean up the environment after each test.

        This function closes the database connection and sets the current database instance to None.

        Parameters:
            self (TestCase): The current instance of the test case.

        Returns:
            None
        """
        # Clean the environment after each test
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
