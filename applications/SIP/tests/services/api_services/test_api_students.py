import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.student import Student
from applications.SIP.modules.utils.fake_data_student_generator import FakeDataStudentGenerator

from applications.SIP.modules.factory.students_factory import StudentFactory
from applications.SIP.modules.services.api_services.api_students import APIStudent

def setup_clean_session():
    """
    Sets up a clean session for the current request.

    This function creates a new request object, sets its attributes, and creates a new response object and a session object. It then connects the session to the request and response objects. The `current` object from `gluon.globals` is used to store the request, response, and session objects for easy access.

    Returns:
        The `current` object which contains the request, response, and session objects.
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

class TestAPIStudent(unittest.TestCase):
    def setUp(self):
        """
        Set up the necessary components for testing.

        This function sets up the necessary components for testing by performing the following steps:
        1. Import the `current` object from `gluon.globals`.
        2. Assign a new `Response` object to `current.response`.
        3. Create a new `DAL` object with the SQLite memory database.
        4. Define the `Student` table using the `Student` model and the `db` object.
        5. Generate 50 fake student records using the `FakeDataStudentGenerator` and the `db` object.
        6. Create a mock object for `SQLFORM.grid` and return "Mock Grid" when called.
        7. Create an instance of the `APIStudent` class with the `db` object and assign it to `self.api_student`.

        This function does not take any parameters and does not have a return value.
        """
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Student(self.db).define_table()
        FakeDataStudentGenerator(self.db).generate_students(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        
        # Here you must define the necessary tables for your tests, such as Student, etc.
        self.api_student = APIStudent(self.db)

    def test_create_student(self):
        """
        Test the create_student method of the APIStudent class.

        This function tests the create_student method of the APIStudent class by attempting to create a new student with the given student_data dictionary. It asserts that the HTTP status code of the response is 201 and the status is 'success'.

        Parameters:
        - self: The instance of the test case.

        Returns:
        - None
        """
        # Try a student creation
        student_data = {'name': 'Juan', 'lastname': 'Pérez', 'email': 'juan@example.com', 'phone': '1234567890'}
        response = self.api_student.create_student(student_data)
        self.assertEqual(response['http_status'], 201)
        self.assertEqual(response['status'], 'success')

    def test_list_student(self):
        """
        Test the functionality of the `list_student` method.

        This function sends a request to the `list_student` API endpoint and asserts that the response has an HTTP status code of 200 and that the `students` field of the response is a list.

        Parameters:
            self (TestClassName): An instance of the test class.

        Returns:
            None
        """
        # Try the student list
        response = self.api_student.list_student()
        self.assertEqual(response['http_status'], 200)
        self.assertIsInstance(response['students'], list)

    def test_get_student(self):
        """
        Try getting a specific student.

        :param self: The current instance of the test class.
        :return: None
        """
        # Try getting a specific student
        student_id = 2  # Make sure this ID exists
        response = self.api_student.get_student(student_id)
        self.assertEqual(response['http_status'], 200)

    def test_update_student(self):
        """
        Try updating a student.

        Args:
            self: The object itself.
        
        Returns:
            None
        """
        # Try updating a student
        student_id = 3  # Make sure this ID exists
        student_data = {'name': 'Ana'}  # Actualización de datos
        response = self.api_student.update_student(student_id, student_data)
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    def test_delete_student(self):
        """
        Delete a student by their ID.

        Args:
            self (TestClass): The instance of the test class.
        
        Returns:
            None
        """
        # Try removing a student
        student_id = 1  # Make sure this ID exists
        response = self.api_student.delete_student(student_id)
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    def test_get_total_students(self):
        """
        Try to get the total number of students.
        """
        # Try to get the total number of students
        response = self.api_student.get_total_students()
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    def tearDown(self):
        """
        Tear down the environment after each test.

        This function closes the database connection.

        Parameters:
            self (TestCase): The test case instance.

        Returns:
            None
        """
        # Clean the environment after each test
        self.db.close()

if __name__ == '__main__':
    unittest.main()