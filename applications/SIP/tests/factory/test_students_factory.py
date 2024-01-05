import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.student import Student
from applications.SIP.modules.utils.fake_data_student_generator import FakeDataStudentGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.students_factory import StudentFactory

def setup_clean_session():
    """
    Set up a clean session for the application.

    This function creates a clean session for the application by initializing
    the necessary objects and variables. It sets up the request, response, and
    session objects using the provided environment and creates a new instance
    of the `Request` and `Response` classes. It then connects the session to
    the request and response objects. Finally, it sets the `request`, `response`,
    and `session` objects in the `current` module and returns the `current`
    module.

    Returns:
        current (module): The `current` module with the `request`, `response`,
        and `session` objects set.
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

class TestStudentFactory(unittest.TestCase):
        
    def setUp(self):
        """
        Set up the necessary objects and data for testing.

        Parameters:
            None

        Returns:
            None
        """
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Student(self.db).define_table()
        FakeDataStudentGenerator(self.db).generate_students(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Initialize the factory
        self.factory = StudentFactory(self.db)

    def test_create_student(self):
        """
        Test the creation of a student.

        This function tests the creation of a student by providing a dictionary of student data
        containing the name, lastname, email, and phone number. It then calls the `get_or_create_student`
        method of the `factory` object with the student data to create the student. Finally, it asserts
        that the student's ID is present in the `cache` attribute of the `factory` object.

        Parameters:
            self (TestCase): The instance of the test case class.
        
        Returns:
            None
        """
        # Try a student creation
        student_data = {'name': 'John', 'lastname': 'Doe', 'email': 'john.doe@example.com', 'phone': '12345678'}
        student = self.factory.get_or_create_student(student_data)
        self.assertIn(student.id, self.factory.cache)

    def test_get_student(self):
        """
        Test the retrieval of a student.

        This function tests the retrieval of a student by creating a student using the provided student data. It then fetches the student using the created student's ID and asserts that the fetched student's ID is equal to the created student's ID.

        Parameters:
        - self: The instance of the class.
        
        Returns:
        - None
        """
        # Test a student's recovery
        student_data = {'name': 'Jane', 'lastname': 'Doe', 'email': 'jane.doe@example.com', 'phone': '33345678'}
        created_student = self.factory.get_or_create_student(student_data)
        fetched_student = self.factory.get_student(created_student.id)
        self.assertEqual(fetched_student.id, created_student.id)

    def test_list_students(self):
        """
        Test the student list.

        Parameters:
            self (object): The current instance of the class.
        
        Returns:
            None
        """
        # Test the student list
        students = self.factory.list_students(1, 10)
        self.assertTrue(len(students) > 0)

    def tearDown(self):
        """
        Tear down method for cleaning up the state after each test.

        This method resets the state of the 'current' object by setting its request,
        response, and session attributes to None. It also closes the database connection
        and sets the 'current.db' attribute to None.

        Parameters:
            self (TestCase): The current test case instance.

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
