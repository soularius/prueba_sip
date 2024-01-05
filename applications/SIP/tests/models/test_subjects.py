import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.subjects import Subjects

class TestSubjectsModel(unittest.TestCase):
    def setUp(self):
        """
        Set up the initial configuration.

        :param self: The instance of the class.
        """
        # Initial setup
        self.db = DAL('sqlite:memory:')
        Subjects(self.db).define_table()
        current.db = self.db

    def test_validation(self):
        """
        Test the validation of creating a record without required fields.
        """
        # Trying to create a record without required fields
        try:
            self.db.subjects.insert()
            self.db.commit()
        except:
            self.db.rollback()

        # Check that the record has not been created
        self.assertEqual(self.db(self.db.subjects).count(), 0)

    def test_update_subject(self):
        """
        Test the update_subject() method.
        """
        # Update a subject
        subject_id = self.db.subjects.insert(name="Matemáticas", description="Estudio de números y formas")
        self.db(self.db.subjects.id == subject_id).update(name="Física")
        updated_subject = self.db.subjects(subject_id)

        # Validate the update
        self.assertEqual(updated_subject.name, "Física")

    def test_delete_subject(self):
        """
        Test the delete_subject method.
        
        This function tests the functionality of the delete_subject method in the class.
        
        Parameters:
            self (object): The current instance of the test class.
        
        Returns:
            None
        """
        # Delete a matter
        subject_id = self.db.subjects.insert(name="Matemáticas", description="Estudio de números y formas")
        self.db(self.db.subjects.id == subject_id).delete()
        deleted_subject = self.db.subjects(subject_id)

        # Validate the deletion
        self.assertIsNone(deleted_subject)

    def tearDown(self):
        """
        Clean the environment after each test.
        """
        # Clean the environment after each test
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
