import unittest
from mock import Mock
from gluon.dal import DAL
from gluon.globals import Request, Response, Session
from gluon import current

from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.attendance_factory import AttendanceFactory

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

class TestAttendanceFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the class for testing.

        This class method is used to set up the necessary database tables and data for testing. It creates the necessary tables for the Student, DayOfWeek, Salons, Schedules, Subjects, Teachers, Classes, ClassesStudents, Attendance, and FakeGenerateController models. It also sets the current database to the in-memory SQLite database.

        Parameters:
        - cls: The class object.

        Returns:
        - None
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
        Set up the test environment for the current test case.
        This function initializes the necessary objects and variables required for the test.

        Parameters:
            None

        Returns:
            None
        """
        from gluon.globals import current
        current.response = Response()

        self.factory = AttendanceFactory(self.db)

    def test_create_attendance(self):
        """
        Test the creation of attendance and check if it is added to the cache.

        :param self: The instance of the test class.
        :return: None
        """
        # Create an attendance and verify that it is added to the cache
        attendance_data = {'classes_students_id': 6, 'date_class': '2023-01-01', 'status': '1', 'note': 'Loremp'}
        attendance = self.factory.get_or_create_attendance(attendance_data)
        self.assertIn(attendance.id, self.factory.cache)

    def test_read_attendance(self):
        """
        Test the functionality of the 'read_attendance' method.

        This method creates and then retrieves an attendance record using the provided attendance data.
        The attendance data should include the 'classes_students_id', 'date_class', 'status', and 'note' fields.

        Parameters:
            self (TestClass): The instance of the test class.
        
        Returns:
            None
        """
        # Create and then retrieve an attendance
        attendance_data = {'classes_students_id': 6, 'date_class': '2023-01-01', 'status': '1', 'note': 'Loremp'}
        created_attendance = self.factory.get_or_create_attendance(attendance_data)
        fetched_attendance = self.factory.get_attendance(created_attendance.id)
        self.assertEqual(fetched_attendance.id, created_attendance.id)

    def test_update_attendance(self):
        """
        This function is used to test the update_attendance method of the Factory class.

        Parameters:
        - self: The instance of the test class.
        
        Returns:
        - None
        """
        # Update an assistance
        attendance_id = 2
        updated_data = {'classes_students_id': 6, 'date_class': '2023-01-01', 'status': '1', 'note': 'Loremp'}
        self.factory.update_attendance(attendance_id, updated_data)
        updated_attendance = self.factory.get_attendance(attendance_id)
        self.assertEqual(updated_attendance.date_class, '2023-01-01')

    def test_delete_attendance(self):
        """
        Delete an attendance record.

        This function takes an attendance ID as a parameter and deletes the corresponding attendance record from the factory cache. It then asserts that the attendance ID is not present in the factory cache.

        Parameters:
        - attendance_id (int): The ID of the attendance record to be deleted.

        Returns:
        - None
        """
        # Delete an assistance
        attendance_id = 4
        self.factory.delete_attendance(attendance_id)
        self.assertNotIn(attendance_id, self.factory.cache)

    def test_list_attendances(self):
        """
        Test the functionality of the `list_attendances` method.

        This function fetches a list of attendances using the `list_attendances` method from the `factory` object and asserts that the length of the returned list is greater than 0.

        Parameters:
        - self: The instance of the class calling this method.

        Returns:
        - None

        Raises:
        - AssertionError: If the length of the attendances list is not greater than 0.
        """
        # List assists
        attendances = self.factory.list_attendances(1, 10)
        self.assertTrue(len(attendances) > 0)

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class by rolling back the database changes and resetting the global variables.

        :param cls: The test class.
        :type cls: class
        :return: None
        :rtype: None
        """
        cls.db.rollback()
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
