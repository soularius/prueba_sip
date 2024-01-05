import unittest
from gluon.dal import DAL
from gluon import current
import datetime

from applications.SIP.modules.models.schedules import Schedules

class TestSchedulesModel(unittest.TestCase):
    def setUp(self):
        """
        Set up the initial environment for the test case.

        Parameters:
            self (TestCase): The current test case object.

        Returns:
            None
        """
        # Initial setup
        self.db = DAL('sqlite:memory:')
        Schedules(self.db).define_table()
        current.db = self.db

    def test_create_schedule(self):
        """
        Test the create_schedule method.

        This test case verifies that the create_schedule method creates a schedule correctly by performing the following steps:
        
        1. Create a schedule using the `block_start` and `block_end` parameters.
        2. Retrieve the created schedule from the database.
        3. Verify that the schedule record is not None.
        4. Verify that the `block_start` attribute of the schedule record is equal to the expected value.
        5. Verify that the `block_end` attribute of the schedule record is equal to the expected value.
        """
        # Create a schedule
        schedule_id = self.db.schedules.insert(block_start="08:00", block_end="10:00")

        # Recover the created schedule
        schedule_record = self.db.schedules(schedule_id)

        # Vverify that the schedule has been created correctly
        self.assertIsNotNone(schedule_record)
        self.assertEqual(schedule_record.block_start, datetime.time(8, 0))
        self.assertEqual(schedule_record.block_end, datetime.time(10, 0))

    def test_validation(self):
        """
        Test the validation of creating a schedule with no start or end time.

        This function tries to create a schedule with no start or end time by inserting a new record into the `schedules` table in the database. If the insertion is successful, the database is committed; otherwise, a rollback is performed. After the operation, the function checks that the schedule has not been created by asserting that the count of records in the `schedules` table is 0.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        # Trying to create a schedule with no start or end time
        try:
            self.db.schedules.insert()
            self.db.commit()
        except:
            self.db.rollback()
        # Check that the schedule has not been created
        self.assertEqual(self.db(self.db.schedules).count(), 0)

    def test_update_schedule(self):
        """
        Updates a schedule.

        Parameters:
            self (object): The current instance of the test class.

        Returns:
            None
        """
        # Update a schedule
        schedule_id = self.db.schedules.insert(block_start="08:00", block_end="10:00")
        self.db(self.db.schedules.id == schedule_id).update(block_start="09:00", block_end="11:00")
        updated_schedule = self.db.schedules(schedule_id)

        # Validate the update
        self.assertEqual(updated_schedule.block_start, datetime.time(9, 0))
        self.assertEqual(updated_schedule.block_end, datetime.time(11, 0))

    def test_delete_schedule(self):
        """
        Delete a schedule and validate the deletion.

        This function creates a new schedule in the database using the provided `block_start`
        and `block_end` values. It then deletes the schedule using the `schedule_id` and
        verifies that the schedule was successfully deleted.

        Parameters:
            self (object): The current instance of the test case.

        Returns:
            None
        """
        # Delete a schedule
        schedule_id = self.db.schedules.insert(block_start="08:00", block_end="10:00")
        self.db(self.db.schedules.id == schedule_id).delete()
        deleted_schedule = self.db.schedules(schedule_id)

        # Validate the deletion
        self.assertIsNone(deleted_schedule)

    def tearDown(self):
        """
        Clean the environment after each test.
        """
        # Clean the environment after each test
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
