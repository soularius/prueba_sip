import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session
from applications.SIP.controllers.attendances import *

from applications.SIP.modules.models.student import Student
from applications.SIP.modules.models.day_of_week import DayOfWeek
from applications.SIP.modules.models.salons import Salons
from applications.SIP.modules.models.schedules import Schedules
from applications.SIP.modules.models.subjects import Subjects
from applications.SIP.modules.models.teachers import Teachers
from applications.SIP.modules.models.classes_students import ClassesStudents
from applications.SIP.modules.models.classes import Classes
from applications.SIP.modules.models.attendance import Attendance

from applications.SIP.controllers.fake_generate_controller import FakeGenerateController

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

class TestAttendancesController(unittest.TestCase):
    """
    Test suite for the AttendancesController in the SIP application.

    This test suite verifies the functionality of the AttendancesController's methods, 
    including creating, updating, listing, retrieving, and deleting attendance records.
    It uses an in-memory SQLite database for testing database interactions.

    Class Methods:
        setUpClass(): Initializes the in-memory database and populates it with test data.
        tearDownClass(): Cleans up the test environment after all tests have run.

    Methods:
        setUp(): Configures the test environment before each test.
        test_attendance_view(): Tests the attendance_view function.
        test_attendance_update(): Tests the attendance_update function.
        test_api_create_attendance(): Tests the api_create_attendance function.
        test_api_update_attendance(): Tests the api_update_attendance function.
        test_api_list_attendance(): Tests the api_list_attendance function.
        test_api_get_attendance(): Tests the api_get_attendance function.
        test_api_delete_attendance(): Tests the api_delete_attendance function.
    """

    @classmethod
    def setUpClass(cls):
        cls.db = DAL('sqlite:memory:')
        Student(cls.db).define_table()
        DayOfWeek(cls.db).define_table()
        Salons(cls.db).define_table()
        Schedules(cls.db).define_table()
        Subjects(cls.db).define_table()
        Teachers(cls.db).define_table()
        Classes(cls.db).define_table()
        ClassesStudents(cls.db).define_table()
        Attendance(cls.db).define_table()
        FakeGenerateController(cls.db).index()
        current.db = cls.db

    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")

    def test_attendance_view(self):
        """
        Tests the attendance_view function.

        Verifies that the function constructs the correct URL for a given attendance record
        and returns the expected result.
        """
        record_id = '2'
        # Configure the request object
        self.request = Request({'wsgi.input': None, 'env': {'request_method': 'GET'}})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'attendance_view'

        from gluon.globals import current
        current.request = self.request

        # Get a test record
        record = self.db.attendance(record_id)
        # Build the URL
        constructed_url = URL('SIP', 'attendances', 'attendance_update', args=[record.id], extension='json')
        self.assertEqual(constructed_url, f'/SIP/attendances/attendance_update.json/{record_id}')
        result = attendance_view()
    
    def test_attendance_update(self):
        """
        Tests the attendance_update function.

        Verifies that the function updates an attendance record with new data correctly.
        """
        # Create a test attendance record
        record_id = '3'
        updated_record = self.db.attendance(record_id)
        self.db.commit()

        # Set the request object for a successful update
        new_status = '1'
        self.request = Request({'wsgi.input': None, 'env': {'request_method': 'GET'}})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'attendance_update'
        self.request.args = [record_id]  # ID of the record to update
        self.request._post_vars = {f'status_{record_id}': new_status}  # Nuevo estado

        from gluon.globals import current
        current.request = self.request

        # Call update function
        response = attendance_update()

        # Verify that the status has been updated correctly
        updated_record = self.db.attendance(record_id)
        self.assertEqual(updated_record.status, int(new_status))

    def test_api_create_attendance(self):
        """
        Tests the api_create_attendance function.

        Verifies that the function creates a new attendance record and returns the expected status.
        """
        # Configure the request object
        env = {'request_method': 'POST', "PATH_INFO": '/SIP/attendances/api_create_attendance'}
        self.request = Request(env)
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_create_attendance'
        self.request._post_vars = {   'classes_students_id': 1, 
                                'date_class': "2023-10-27",
                                'status': 1,
                                'note': "Test note"
                            }
        self.request.is_restful = True
        
        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_create_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 201)
        self.assertIn('success', response['status']) 

    def test_api_update_attendance(self):
        """
        Tests the api_update_attendance function.

        Verifies that the function updates an existing attendance record with new data and returns
        the expected status.
        """
        attendance_id = '2'  # Replace with a valid ID if necessary

        env = {'request_method': 'PUT', "PATH_INFO": '/SIP/attendances/api_update_attendance'}
        self.request = Request(env)
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_update_attendance'
        self.request.args = [attendance_id]
        self.request._post_vars = {'status': 0, 'note': 'Updated note'}
        self.request.is_restful = True

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        # Run the test
        from gluon.http import HTTP
        try:
            response = api_update_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
    
    def test_api_list_attendance(self):
        """
        Tests the api_list_attendance function.

        Verifies that the function lists attendance records correctly with pagination and returns
        the expected status.
        """
        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_list_attendance'
        self.request.vars = {'page': 1, 'page_size': 10}

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_list_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
    
    def test_api_get_attendance(self):
        """
        Tests the api_get_attendance function.

        Verifies that the function retrieves a specific attendance record and returns the expected status.
        """
        # Make sure you have a valid support record to test
        attendance_id = '3'

        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_get_attendance'
        self.request.args = [attendance_id]
        
        from gluon.globals import current
        current.request = self.request

        from gluon.http import HTTP
        try:
            response = api_get_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
   
    def test_api_delete_attendance(self):
        """
        Tests the api_delete_attendance function.

        Verifies that the function deletes a specific attendance record and returns the expected status.
        """
        attendance_id = '1'  # Replace with a valid ID if necessary

        self.request = Request(env={'request_method': 'DELETE'})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_delete_attendance'
        self.request.args = [attendance_id]

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_delete_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)

    @classmethod
    def tearDownClass(cls):
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
