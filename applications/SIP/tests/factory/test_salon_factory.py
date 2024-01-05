import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.salons import Salons
from applications.SIP.modules.utils.fake_data_salons_generator import FakeDataSalonGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.salon_factory import SalonFactory

def setup_clean_session():
    """
    Set up a clean session for the current request.

    Returns:
        `current`: The current request, response, and session objects.
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

class TestSalonFactory(unittest.TestCase):
        
    def setUp(self):
        """
        Set up the necessary environment for the test case.

        This function initializes the following components:
        - `current.response` is set to an instance of `Response` from the `gluon.globals` module.
        - `self.db` is initialized as an instance of `DAL` with a SQLite in-memory database.
        - The `Salons` table is defined in the database using the `define_table` method of the `Salons` class.
        - 50 fake salon records are generated in the database using the `generate_salons` method of the `FakeDataSalonGenerator` class.
        - `self.SQLFORM.grid` is mocked using the `Mock` class and set to return the string "Mock Grid".
        - The `self.factory` attribute is initialized as an instance of the `SalonFactory` class with `self.db` as the argument.

        This function is part of a test case and is executed before each test method is run.
        """
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Salons(self.db).define_table()
        FakeDataSalonGenerator(self.db).generate_salons(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Initialize the factory
        self.factory = SalonFactory(self.db)

    def test_create_salon(self):
        """
        Test the creation of a salon.

        Parameters:
            - None

        Returns:
            - None
        """
        # Try creating a room
        salon_data = {'name': 'A101', 'description': 'Math Class'}
        salon = self.factory.get_or_create_salon(salon_data)
        self.assertIn(salon.id, self.factory.cache)

    def test_get_salon(self):
        """
        Test the get_salon method of the factory class.

        This function tests the functionality of the get_salon method of the factory class.
        It creates a salon using the get_or_create_salon method and then fetches the salon
        using the get_salon method. Finally, it asserts that the fetched salon id is equal
        to the created salon id.

        Parameters:
            self (TestFactory): The instance of the TestFactory class.

        Returns:
            None
        """
        # Try recovering a room
        salon_data = {'name': 'B202', 'description': 'Physics Lab'}
        created_salon = self.factory.get_or_create_salon(salon_data)
        fetched_salon = self.factory.get_salon(created_salon.id)
        self.assertEqual(fetched_salon.id, created_salon.id)

    def test_list_salons(self):
        """
        Test the functionality of the list_salons method.

        Returns:
            None
        """
        # Try the list of salons
        salons = self.factory.list_salons()
        self.assertTrue(len(salons) > 0)

    def tearDown(self):
        """
        Tear down the test environment after each test.

        This function resets the state of 'current' after each test. It sets the following properties of 'current' to None: request, response, and session. It also closes the database connection and sets 'current.db' to None.

        This function does not take any parameters and does not return anything.
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
