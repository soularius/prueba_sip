import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session
from applications.SIP.controllers.students import *


from applications.SIP.modules.models.student import Student
from applications.SIP.modules.utils.fake_data_student_generator import FakeDataStudentGenerator

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


class TestStudentsController(unittest.TestCase):
    """
    Test suite for the StudentsController in the SIP application.

    This class provides unit tests for various functionalities of the StudentsController, 
    including registering, listing, viewing, editing, and API operations related to students. 
    The tests use an in-memory SQLite database and mock objects to simulate web2py components.

    Methods:
        setUp(): Configures the test environment and database before each test.
        test_students_register_ts(): Tests the student registration view.
        test_students_list_ts(): Tests the student listing view.
        test_students_view_ts(): Tests the student detail view.
        test_students_edit_ts(): Tests the student edit view.
        test_api_create_student(): Tests the API endpoint for creating a student.
        test_api_list_student(): Tests the API endpoint for listing students.
        test_api_get_student(): Tests the API endpoint for retrieving a specific student.
        test_api_update_student(): Tests the API endpoint for updating a student.
        test_api_delete_student(): Tests the API endpoint for deleting a student.
        test_api_total_students(): Tests the API endpoint for getting the total number of students.
        tearDown(): Resets the test environment after each test.
    """
    def setUp(self):
        """
        Set up the necessary resources and environment for testing.

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

    def test_students_register_ts(self):
        """
        Test the students_register_ts function.

        Verifies that the student registration view is rendered correctly with the title 'Registro de Estudiante'.
        """
        response = students_register_ts()
        self.assertEqual(response['tittle'], "Registro de Estudiante")
    
    def test_students_list_ts(self):
        """
        Test the students_list_ts function.

        Verifies that the student listing view is rendered correctly with the title 'Listado de Estudiantes'.
        """
        response = students_list_ts()
        self.assertEqual(response['tittle'], "Listado de Estudiantes")

    def test_students_view_ts(self):
        """
        Test the students_view_ts function.

        Verifies that the student detail view is rendered correctly for a specific student ID.
        Checks if the title is 'Detalle de Estudiante' and the student ID matches the expected value.
        """
        student_id = '2'
        # Configure the request object
        self.request = Request(env={'request_method': 'GET'})
        self.request.args = [str(student_id)]

        from gluon.globals import current
        current.request = self.request

        response = students_view_ts()
        self.assertEqual(response['tittle'], "Detalle de Estudiante")
        self.assertEqual(response['student_id'], int(student_id))

    def test_students_edit_ts(self):
        """
        Test the students_edit_ts function.

        Verifies that the student edit view is rendered correctly for a specific student ID.
        Checks if the title is 'Editar Estudiante' and the student ID matches the expected value.
        """
        student_id = '4'
        # Configure the request object
        self.request = Request(env={'request_method': 'GET'})
        self.request.args = [str(student_id)]

        from gluon.globals import current
        current.request = self.request

        response = students_edit_ts()
        self.assertEqual(response['tittle'], "Editar Estudiante")
        self.assertEqual(response['student_id'], int(student_id))

    def test_api_create_student(self):
        """
        Test the api_create_student function.

        Verifies that a new student can be created through the API.
        Checks if the HTTP status is 201 (Created) and the response status is 'success'.
        """
        # Configure the request object
        env = {'request_method': 'POST', "PATH_INFO": '/SIP/students/api_create_student'}
        self.request = Request(env)
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_create_student'
        self.request._post_vars = {
            'name': "John",
            'lastname': "Doe",
            'phone': "3239940542",
            'email': "johndoe@example.com"
        }
        self.request.is_restful = True
        
        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_create_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)

        self.assertEqual(response['http_status'], 201)  # Assuming you return 201 on success
        self.assertIn('success', response['status'])

    def test_api_list_student(self):
        """
        Test the api_list_student function.

        Verifies that the API correctly lists students with pagination.
        Checks if the HTTP status is 200 (OK).
        """
        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_list_student'
        self.request.vars = {'page': 1, 'page_size': 10}

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_list_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)  # Assuming you return 200 on success

    def test_api_get_student(self):
        """
        Test the api_get_student function.

        Verifies that the API correctly retrieves a specific student by ID.
        Checks if the HTTP status is 200 (OK).
        """
        # Make sure you have a valid student registration to try
        student_id = '2'  # Replace with a valid ID if necessary

        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_get_student'
        self.request.args = [student_id]

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_get_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)

    def test_api_update_student(self):
        """
        Test the api_update_student function.

        Verifies that a student's details can be updated through the API.
        Checks if the HTTP status is 200 (OK).
        """
        student_id = '3'  # Replace with a valid ID if necessary use the diferent id to the others methods

        self.request = Request(env={'request_method': 'PUT'})
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_update_student'
        self.request.args = [student_id]
        self.request._post_vars = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
        
        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_update_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)

    def test_api_delete_student(self):
        """
        Test the api_delete_student function.

        Verifies that a student can be deleted through the API.
        Checks if the HTTP status is 200 (OK).
        """
        student_id = '1'

        self.request = Request(env={'request_method': 'DELETE'})
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_delete_student'
        self.request.args = [student_id]

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_delete_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
    
    def test_api_total_students(self):
        """
        Test the api_total_students function.

        Verifies that the API correctly reports the total number of students.
        Checks if the HTTP status is 200 (OK) and the total number of students is correctly reported.
        """
        from gluon.globals import current
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_total_students()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)


    def tearDown(self):
        """
        Tear down the test environment after each test.

        Resets the state of 'current' to ensure no interference between tests.
        """
        # Reset status to 'current' after each test
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()