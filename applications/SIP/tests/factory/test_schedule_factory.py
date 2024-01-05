import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.schedules import Schedules
from applications.SIP.modules.utils.fake_data_schedules_generator import FakeDataScheduleGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.schedule_factory import ScheduleFactory

def setup_clean_session():
    request = Request(env={})
    request.application = "a"
    request.controller = "c"
    request.function = "f"
    request.folder = "applications/SIP"
    response = Response()
    session = Session()
    session.connect(request, response)
    from gluon.globals import current

    current.request = request
    current.response = response
    current.session = session
    return current

class TestScheduleFactory(unittest.TestCase):
        
    def setUp(self):
        """
        Set up the necessary resources and dependencies for the test case.

        This function initializes the following:

        - The `current.response` variable from the `gluon.globals` module.
        - The `self.db` variable as an instance of a SQLite database connection.
        - The `Schedules` table in the database using the `define_table` method of the `Schedules` class.
        - Fifty fake schedules using the `generate_schedules` method of the `FakeDataScheduleGenerator` class.
        - The `self.SQLFORM.grid` attribute as a mock object that returns the string "Mock Grid".
        - The `self.factory` attribute as an instance of the `ScheduleFactory` class.

        It does not take any parameters and does not return anything.
        """
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Schedules(self.db).define_table()
        FakeDataScheduleGenerator(self.db).generate_schedules(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Initialize the factory
        self.factory = ScheduleFactory(self.db)

    def test_create_schedule(self):
        """
        Try creating a schedule.

        :param self: The instance of the test case.
        :return: None
        """
        # Try creating a schedule
        schedule_data = {'block_start': '08:00', 'block_end': '10:00'}
        schedule = self.factory.get_or_create_schedule(schedule_data)
        self.assertIn(schedule.id, self.factory.cache)

    def test_get_schedule(self):
        """
        Test the retrieval of a schedule.

        This function tests the get_or_create_schedule method of the factory class.
        It creates a schedule with the given schedule_data, retrieves it using the
        get_schedule method, and asserts that the retrieved schedule's id is equal
        to the created schedule's id.

        Parameters:
        - self: The instance of the test class.

        Returns:
        - None
        """
        # Try recovering a schedule
        schedule_data = {'block_start': '10:00', 'block_end': '12:00'}
        created_schedule = self.factory.get_or_create_schedule(schedule_data)
        fetched_schedule = self.factory.get_schedule(created_schedule.id)
        self.assertEqual(fetched_schedule.id, created_schedule.id)

    def test_list_schedules(self):
        """
        Test the function list_schedules.

        This function tests the list_schedules method of the factory object. 
        It calls the list_schedules method and checks if the returned schedules list is not empty.

        Parameters:
            self (TestCase): The current test case.

        Returns:
            None
        """
        # Try the schedule list
        schedules = self.factory.list_schedules()
        self.assertTrue(len(schedules) > 0)

    def tearDown(self):
        """
        Tear down method that resets the state of 'current' after each test.

        This method performs the following actions:
        - Resets the 'request' attribute of the 'current' object to None.
        - Resets the 'response' attribute of the 'current' object to None.
        - Resets the 'session' attribute of the 'current' object to None.
        - Closes the database connection.
        - Resets the 'db' attribute of the 'current' object to None.

        Parameters:
            self: The current instance of the test class.

        Return:
            None
        """
        # Reset status to 'current' after each test
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
