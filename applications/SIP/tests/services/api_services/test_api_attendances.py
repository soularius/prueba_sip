import unittest
from mock import Mock
from gluon.dal import DAL
from gluon.globals import Request, Response, Session
from gluon import current

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

from applications.SIP.modules.factory.attendance_factory import AttendanceFactory
from applications.SIP.modules.services.api_services.api_attendances import APIAttendance

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

class TestAPIAttendance(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """
        Set up the class for testing by creating necessary tables and initializing the database.

        This class method is responsible for setting up the testing environment by performing the following actions:
        1. Create the necessary tables in the in-memory SQLite database.
        2. Define the tables for the 'Student', 'DayOfWeek', 'Salons', 'Schedules', 'Subjects', 'Teachers', 'Classes', 'ClassesStudents', and 'Attendance' models.
        3. Invoke the 'index' method of the 'FakeGenerateController' to generate fake data.
        4. Set the class variable 'db' to the initialized database.

        Parameters:
            cls (class): The class object representing the test case.

        Returns:
            None
        """
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
        """
        Set up the necessary tables and objects for testing purposes.
        """
        from gluon.globals import current
        current.response = Response()

        # Here you must define the necessary tables for your tests, such as Attendance, etc.
        self.api_attendance = APIAttendance(self.db)

    def test_create_attendance(self):
        """
        Test the creation of an attendance.

        This function tests the creation of an attendance by calling the `create_attendance` method of the `api_attendance` object.
        
        Parameters:
            self: The current object.
        
        Returns:
            None.
        """
        # Try creating an assistance
        attendance_data = {'classes_students_id': 1, 'date_class': '2023-01-01', 'status': 1, 'note': 'Present'}
        response = self.api_attendance.create_attendance(attendance_data)
        self.assertEqual(response['http_status'], 201)
        self.assertEqual(response['status'], 'success')

    def test_list_attendance(self):
        """
        Test the 'list_attendance' method of the 'api_attendance' object.

        Asserts that the HTTP status of the response is 200 and that the 'attendances'
        attribute of the response is a list.
        """
        # Try the assistance list
        response = self.api_attendance.list_attendance()
        self.assertEqual(response['http_status'], 200)
        self.assertIsInstance(response['attendances'], list)

    def test_get_attendance(self):
        """
        Test the get_attendance method of the APIAttendance class.

        This function tries to get the attendance data for a specific ID.
        It verifies that the HTTP status code returned is 200.

        Parameters:
        - self: The instance of the test case class.

        Returns:
        - None
        """
        # Try getting specific assistance
        attendance_id = 1  # Make sure this ID exists
        response = self.api_attendance.get_attendance(attendance_id)
        self.assertEqual(response['http_status'], 200)

    def test_update_attendance(self):
        """
        Update the attendance for a specific assistance.

        Parameters:
            self (object): The current instance of the class.
        
        Returns:
            None
        """
        # Try updating an assistance
        attendance_id = 1  # Make sure this ID exists
        attendance_data = {'status': 0}  # Data update
        response = self.api_attendance.update_attendance(attendance_id, attendance_data)
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    def test_delete_attendance(self):
        """
        Test the delete_attendance method.

        This method tries to remove an attendance record from the API by providing
        an attendance ID. The attendance ID should exist in the system for the deletion
        to be successful.

        :param self: The current instance of the test class.
        :return: None
        """
        # Try removing an assist
        attendance_id = 2  # Make sure this ID exists
        response = self.api_attendance.delete_attendance(attendance_id)
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    @classmethod
    def tearDownClass(cls):
        """
        This method is used to tear down the test class after all the tests have been executed. It resets the global variables related to the Gluon framework.

        Parameters:
            cls (class): The class object.

        Returns:
            None
        """
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
