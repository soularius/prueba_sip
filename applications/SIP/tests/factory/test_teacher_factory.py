import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.teachers import Teachers
from applications.SIP.modules.utils.fake_data_teacher_generator import FakeDataTeacherGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.teacher_factory import TeacherFactory

def setup_clean_session():
    """
    Initializes the necessary objects and variables for a clean session.

    :return: The current session object.
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

class TestTeacherFactory(unittest.TestCase):
        
    def setUp(self):
        """
        Set up the necessary environment for testing.

        This function initializes the necessary components for testing. It sets up the current response object, creates an in-memory SQLite database, defines a table for teachers in the database, generates 50 fake teachers using the FakeDataTeacherGenerator, and initializes the SQLFORM grid and TeacherFactory.

        Parameters:
            None

        Returns:
            None
        """
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Teachers(self.db).define_table()
        FakeDataTeacherGenerator(self.db).generate_teachers(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Initialize the factory
        self.factory = TeacherFactory(self.db)

    def test_create_teacher(self):
        """
        Test the creation of a teacher.

        Parameters:
            self (TestCase): The current test case.
        
        Returns:
            None
        """
        # Try creating a teacher
        teacher_data = {'name': 'John', 'lastname': 'Doe', 'phone': '123456789', 'email': 'johndoe@example.com'}
        teacher = self.factory.get_or_create_teacher(teacher_data)
        self.assertIn(teacher.id, self.factory.cache)

    def test_get_teacher(self):
        """
        Test the retrieval of a teacher.

        This function tests the retrieval of a teacher by performing the following steps:
        
        1. Create a teacher with the provided teacher data.
        2. Retrieve the created teacher using its ID.
        3. Assert that the retrieved teacher's ID matches the created teacher's ID.

        Parameters:
        - None

        Returns:
        - None
        """
        # Try a teacher's recovery
        teacher_data = {'name': 'Jane', 'lastname': 'Smith', 'phone': '987654321', 'email': 'janesmith@example.com'}
        created_teacher = self.factory.get_or_create_teacher(teacher_data)
        fetched_teacher = self.factory.get_teacher(created_teacher.id)
        self.assertEqual(fetched_teacher.id, created_teacher.id)

    def test_list_teachers(self):
        """
        Test case for the `list_teachers` method.

        This test case checks if the `list_teachers` method of the `factory` object
        returns a non-empty list of teachers.

        Parameters:
        - self: The current instance of the test case.

        Returns:
        - None
        """
        # Try the list of teachers
        teachers = self.factory.list_teachers()
        self.assertTrue(len(teachers) > 0)

    def tearDown(self):
        """
        Reset the status to 'current' after each test.

        This function is called after each test is executed in order to reset the status to 'current'. It performs the following tasks:
        - Resets the `current.request` object to `None`.
        - Resets the `current.response` object to `None`.
        - Resets the `current.session` object to `None`.
        - Closes the database connection using `self.db.close()`.
        - Resets the `current.db` object to `None`.
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

