import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.day_of_week import DayOfWeek

class TestDayOfWeekModel(unittest.TestCase):
    def setUp(self):
        """
        Set up the initial configuration.

        This function initializes the database and defines the 'DayOfWeek' table.
        The database is set to an in-memory SQLite database.
        
        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        # Initial setup
        self.db = DAL('sqlite:memory:')
        DayOfWeek(self.db).define_table()
        current.db = self.db

    def test_create_day_of_week(self):
        """
        Test case for creating a new day of the week.

        It creates a new record in the 'day_of_week' table with the name "Lunes". 
        Then, it retrieves the created record and validates that it has been created correctly.
        The name of the created record is asserted to be "Lunes".

        Parameters:
            self (TestCase): The current test case object.

        Returns:
            None
        """
        # Create a record on 'day_of_week'
        day_id = self.db.day_of_week.insert(name="Lunes")

        # Retrieve the created record
        day_record = self.db.day_of_week(day_id)

        # Validate that the record was created correctly
        self.assertIsNotNone(day_record)
        self.assertEqual(day_record.name, "Lunes")

    def test_validation(self):
        """
        Test the validation of the function.

        This function attempts to create a record without a name. It then checks 
        that the record has not been created by asserting that the count of 
        records in the 'day_of_week' table is 0.
        """
        # Try to create a record without a name
        try:
            self.db.day_of_week.insert()
            self.db.commit()
        except:
            self.db.rollback()
        # Check that the record has not been created
        self.assertEqual(self.db(self.db.day_of_week).count(), 0)

    def test_label(self):
        """
        Test the label of the 'name' field.
        """
        # Check the label of the 'name' field
        self.assertEqual(self.db.day_of_week.name.label, 'Día de la semana')

    def tearDown(self):
        """
        Tears down the environment after each test.

        This function closes the database connection and sets the current database object to None.

        Parameters:
            self: The test case object.

        Returns:
            None
        """
        # Clean the environment after each test
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
