import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.subjects import Subjects
from applications.SIP.modules.utils.fake_data_subjects_generator import FakeDataSubjectGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.subject_factory import SubjectFactory

def setup_clean_session():
    """
    Sets up a clean session for the application.

    Returns:
        The current application, response, and session objects.
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

class TestSubjectFactory(unittest.TestCase):
        
    def setUp(self):
        """
        Set up the environment for the test case.
        
        This function initializes the necessary dependencies and resources for the test case. It performs the following actions:
        
        - Imports the `current` object from the `gluon.globals` module.
        - Creates an instance of the `Response` class and assigns it to `current.response`.
        - Creates an instance of the `DAL` class with the SQLite memory database URL and assigns it to `self.db`.
        - Defines the necessary table using the `Subjects` class and the `define_table` method.
        - Generates 50 fake subjects using the `FakeDataSubjectGenerator` class and the `generate_subjects` method.
        - Creates a mock instance of the `SQLFORM` class and assigns it to `self.SQLFORM`.
        - Mocks the `grid` method of the `SQLFORM` class to return the string "Mock Grid".
        - Initializes the `factory` attribute with an instance of the `SubjectFactory` class and `self.db` as the argument.
        
        This function does not have any parameters and does not return any value.
        """
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Subjects(self.db).define_table()
        FakeDataSubjectGenerator(self.db).generate_subjects(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")

        # Initialize the factory
        self.factory = SubjectFactory(self.db)

    def test_create_subject(self):
        """
        Test the creation of a subject.

        This function tests the creation of a subject by calling the `get_or_create_subject` method of the `factory` object. It passes a dictionary `subject_data` with the properties `name` and `description` to specify the subject's name and description. After the subject is created, it checks if the subject's `id` is present in the `cache` attribute of the `factory` object.

        Parameters:
            self (TestCase): The current test case object.

        Returns:
            None
        """
        # Try creating a subject
        subject_data = {'name': 'Math', 'description': 'Mathematics subject'}
        subject = self.factory.get_or_create_subject(subject_data)
        self.assertIn(subject.id, self.factory.cache)

    def test_get_subject(self):
        """
        Test the recovery of a subject.

        Parameters:
        - self: The current object.
        - subject_data: A dictionary containing the subject's name and description.

        Returns:
        - None
        """
        # Test the recovery of a subject
        subject_data = {'name': 'Physics', 'description': 'Physics subject'}
        created_subject = self.factory.get_or_create_subject(subject_data)
        fetched_subject = self.factory.get_subject(created_subject.id)
        self.assertEqual(fetched_subject.id, created_subject.id)

    def test_list_subjects(self):
        """
        Test the list of subjects.
        """
        # Try the list of subjects
        subjects = self.factory.list_subjects()
        self.assertTrue(len(subjects) > 0)

    def tearDown(self):
        """
        Tear down method to reset the state of 'current' after each test.

        This method resets the 'current' object by setting its request, response,
        and session attributes to None. It also closes the database connection
        and sets the 'current.db' attribute to None.

        Parameters:
            self (TestClass): The instance of the test class.

        Returns:
            None
        """
        # Restablecer el estado de 'current' después de cada prueba
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
