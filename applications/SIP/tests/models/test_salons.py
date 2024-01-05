import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.salons import Salons

class TestSalonsModel(unittest.TestCase):
    def setUp(self):
        """
        Set up the initial configuration for the test case.

        This function initializes the `db` attribute with a `DAL` object that connects to an in-memory SQLite database. It also defines a `Salons` table in the database using the `define_table` method. Finally, it sets the `current.db` attribute to the initialized `db` object.

        Parameters:
        - self: The instance of the test case class.

        Returns:
        - None
        """
        # Initial setup
        self.db = DAL('sqlite:memory:')
        Salons(self.db).define_table()
        current.db = self.db

    def test_create_salon(self):
        """
        Test the creation of a salon record.

        This function creates a record in the 'salons' collection with the name "Salón 101" and the description "Salón de clases principal".
        It then retrieves the created record and validates that it exists and has the correct name and description.

        Parameters:
        - self: The instance of the test class.

        Returns:
        - None
        """
        # Create a record in 'salons'
        salon_id = self.db.salons.insert(name="Salón 101", description="Salón de clases principal")

        # Retrieve the created record
        salon_record = self.db.salons(salon_id)

        # Validate that the record was created correctly
        self.assertIsNotNone(salon_record)
        self.assertEqual(salon_record.name, "Salón 101")
        self.assertEqual(salon_record.description, "Salón de clases principal")

    def test_validation(self):
        """
        Test the validation of the function.

        This function attempts to create a record without a name or description. It then checks that the record was not created by asserting that the count of records in the `salons` table is 0.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        # Trying to create a record without a name or description
        try:
            self.db.salons.insert()
            self.db.commit()
        except:
            self.db.rollback()

        # Check that the record has not been created
        self.assertEqual(self.db(self.db.salons).count(), 0)

    def test_update_salon(self):
        """
        Test the update_salon function.

        This function tests the functionality of the update_salon function. It creates a new salon with the name "Salón 101" and description "Salón de clases principal" using the self.db.salons.insert() method. Then, it updates the name of the salon to "Salón 102" using the self.db().update() method. Finally, it retrieves the updated salon using the self.db.salons() method and asserts that the updated salon has the correct name.

        Parameters:
        - self: The test case instance.

        Returns:
        None
        """
        # Update a living room
        salon_id = self.db.salons.insert(name="Salón 101", description="Salón de clases principal")
        self.db(self.db.salons.id == salon_id).update(name="Salón 102")
        updated_salon = self.db.salons(salon_id)

        # Validate the update
        self.assertEqual(updated_salon.name, "Salón 102")

    def test_delete_salon(self):
        """
        Test the deletion of a salon.

        This function tests the functionality of deleting a salon from the database. It creates a new salon with the name "Salón 101" and the description "Salón de clases principal". After creating the salon, it deletes it using the salon's ID. Finally, it verifies that the salon has been deleted by checking that the deleted salon is None.

        Parameters:
        - self: The instance of the test class.

        Returns:
        - None
        """
        # Delete a room
        salon_id = self.db.salons.insert(name="Salón 101", description="Salón de clases principal")
        self.db(self.db.salons.id == salon_id).delete()
        deleted_salon = self.db.salons(salon_id)

        # Validate the deletion
        self.assertIsNone(deleted_salon)

    def tearDown(self):
        """
        Clean up the environment after each test.
        """
        # Clean the environment after each test
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
