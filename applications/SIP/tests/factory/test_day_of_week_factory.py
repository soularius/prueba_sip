import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.day_of_week import DayOfWeek
from applications.SIP.modules.utils.fake_data_day_of_week_generator import FakeDataDayOfWeekGenerator

from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.day_of_week_factory import DayOfWeekFactory

def setup_clean_session():
    """
    Sets up a clean session for the application.
    
    This function creates a new `Request` object with an empty `env` dictionary and sets the `application`, `controller`, `function`, and `folder` attributes to "a", "c", "f", and "applications/SIP" respectively. It also creates a new `Response` object, a new `Session` object, and connects the session to the request and response. Finally, it imports `current` from `gluon.globals` and sets the `request`, `response`, and `session` attributes of `current` to the respective objects. The function returns the `current` object.
    
    Returns:
        `current`: The `current` object with the `request`, `response`, and `session` attributes set.
    """
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

class TestDayOfWeekFactory(unittest.TestCase):
        
    def setUp(self):
        """
        Set up the necessary environment for the unit test.

        This function initializes the necessary objects and variables for the unit test. It performs the following tasks:
        1. Imports the current module from the `gluon.globals` package.
        2. Assigns a new instance of the `Response()` class to the `current.response` object.
        3. Creates a new SQLite in-memory database using the `DAL()` function from the `gluon.dal` package.
        4. Defines a new table named "DayOfWeek" using the `define_table()` method of the `DayOfWeek` class.
        5. Generates fake data for the "DayOfWeek" table using the `generate_days_of_week()` method of the `FakeDataDayOfWeekGenerator` class.
        6. Creates a new instance of the `Mock()` class and assigns it to the `SQLFORM` attribute of the current object.
        7. Sets the return value of the `grid()` method of the `SQLFORM` object to "Mock Grid".
        8. Initializes the `factory` attribute of the current object with a new instance of the `DayOfWeekFactory` class, passing the `db` attribute as a parameter.

        Parameters:
            None

        Returns:
            None
        """
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        DayOfWeek(self.db).define_table()
        FakeDataDayOfWeekGenerator(self.db).generate_days_of_week()

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Initialize the factory
        self.factory = DayOfWeekFactory(self.db)

    def test_create_day_of_week(self):
        """
        Test the creation of a day of the week.

        Parameters:
        - self: The reference to the current object.
        
        Returns:
        - None
        
        Raises:
        - AssertionError: If the day id is not found in the factory cache.
        """
        # Try creating a day of the week
        day_data = {'name': 'Monday'}
        day = self.factory.get_or_create_day_of_week(day_data)
        self.assertIn(day.id, self.factory.cache)

    def test_get_day_of_week(self):
        """
        Test the retrieval of a day of the week.

        This function tests the retrieval of a day of the week using the
        `get_or_create_day_of_week` and `get_day_of_week` methods of the `factory`
        object. It creates a `day_data` dictionary with the name of the day as 'Tuesday',
        then calls the `get_or_create_day_of_week` method to create a day of the week
        record with this name. It then retrieves the day of the week using the
        `get_day_of_week` method and compares the IDs of the retrieved and created
        day of the week records using the `assertEqual` method.

        Parameters:
        - self: The instance of the test class.

        Returns:
        - None
        """
        # Try one day of the week recovery
        day_data = {'name': 'Tuesday'}
        created_day = self.factory.get_or_create_day_of_week(day_data)
        fetched_day = self.factory.get_day_of_week(created_day.name)
        self.assertEqual(fetched_day.id, created_day.id)

    def test_list_days_of_week(self):
        """
        Test the list of days of the week.

        This function tests the list_days_of_week method of the factory object. It checks if the returned list has at least one element.

        Parameters:
            self (TestClass): The instance of the test class.

        Returns:
            None
        """
        # Try the list of days of the week
        days = self.factory.list_days_of_week()
        self.assertTrue(len(days) > 0)

    def tearDown(self):
        """
        Tear down function for cleaning up after each test.

        This function resets the state of 'current' after each test by setting the
        request, response, session, and db attributes of the 'current' object to None.

        Parameters:
            None

        Returns:
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