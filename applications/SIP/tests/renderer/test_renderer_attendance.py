import unittest
from mock import Mock
from gluon import DAL, URL
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

from applications.SIP.modules.renderer.renderer_attendance import RendererAttendance

def setup_clean_session():
    """
    Generates the necessary objects to set up a clean session for the application.

    Returns:
        The current object with the request, response, and session objects set.
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

class TestRendererAttendance(unittest.TestCase):
    """
    Test suite for the RendererAttendance class in the SIP application.

    This class provides unit tests for RendererAttendance, focusing on verifying the functionality
    of rendering attendance records and retrieving related data like student names, salon names, and subject names.
    It uses an in-memory SQLite database for testing database interactions.

    Class Methods:
        setUpClass(): Initializes the in-memory database and populates it with test data.
        tearDownClass(): Cleans up the test environment after all tests have run.

    Methods:
        setUp(): Configures the test environment before each test.
        test_render_view(): Tests the render_view method of RendererAttendance.
        test_get_student_name(): Tests the get_student_name method.
        test_get_salon_name(): Tests the get_salon_name method.
        test_get_subject_name(): Tests the get_subject_name method.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class by creating necessary database tables and generating static data.

        This class method is called before any tests in the test case are executed. It creates a SQLite in-memory database and defines tables for the following models: Student, DayOfWeek, Salons, Schedules, Subjects, Teachers, Classes, ClassesStudents, and Attendance. It then calls the `static_data_generate()` method of the `FakeGenerateController` class to generate fake data in the tables. Finally, it sets the `db` attribute of the class to the created database.

        Parameters:
        - cls: The class itself.

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
        FakeGenerateController(cls.db).static_data_generate()
        FakeGenerateController(cls.db).index()
        current.db = cls.db
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.renderer = RendererAttendance(self.db)

    def test_render_view(self):
        """
        This function is used to test the rendering of a view. It performs the following steps:
        
        - Creates a mock request object with the necessary attributes.
        - Sets the current request object using the mock request.
        - Retrieves attendance records from the database.
        - Renders the view using the attendance records.
        - Decodes the result from XML to a string.
        - Validates that the rendered view contains the expected data.
        
        This function does not take any parameters and does not return anything.

        Verifies that the method correctly renders attendance records into an HTML table.
        Checks if the table contains correct data for students, salons, subjects, and attendance controls.
        """
        self.request = Request({'wsgi.input': None, 'env': {'request_method': 'GET'}})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'attendance_view'

        from gluon.globals import current
        current.request = self.request
        # Retrieve attendance records and generate table
        attendance = self.db.attendance(1)
        attendance_records = self.db(self.db.attendance).select()
        result = self.renderer.render_view(attendance_records)
        
        # Decode XML result to a character string
        result_str = result.xml().decode("utf-8")

        # Validate that the table contains the correct data
        self.assertIn('Marta Salcedo', result_str)
        self.assertIn('A63', result_str)
        self.assertIn('Fisica', result_str)
        self.assertIn('<select', result_str)

    def test_get_student_name(self):
        """
        Test the get_student_name method.

        This function retrieves the list of students from the database and then calls the
        get_student_name method of the renderer object to get the name of the student
        associated with the given classes_students_record. Finally, it asserts that the
        retrieved student name is equal to the expected value.
        Verifies that the method correctly retrieves a student's name given a classes_students record.

        Parameters:
        - self: The current instance of the test class.

        Returns:
        - None
        """
        students = self.db(self.db.students).select()
        # Try the get_student_name method
        classes_students_record = self.db.classes_students(1)
        student_name = self.renderer.get_student_name(classes_students_record)
        self.assertEqual(student_name, "Marta Salcedo")

    def test_get_salon_name(self):
        """
        Test the get_salon_name method.

        This function tests the get_salon_name method of the renderer class. It does the following:
        - Retrieves the classes_students record from the database for class 1.
        - Calls the get_salon_name method of the renderer class with the retrieved classes_students record.
        - Asserts that the returned salon_name is equal to "A63".
        Verifies that the method correctly retrieves a salon's name given a classes_students record.

        Parameters:
        - self: The instance of the test class.

        Return:
        - None
        """
        # Try the get_salon_name method
        classes_students_record = self.db.classes_students(1)
        salon_name = self.renderer.get_salon_name(classes_students_record)
        self.assertEqual(salon_name, "A63")

    def test_get_subject_name(self):
        """
        Test the `get_subject_name` method. Verifies that the method correctly retrieves a subject's
        name given a classes_students record.

        :param self: The current instance of the test class.
        :return: None.
        """
        # Try the get_subject_name method
        classes_students_record = self.db.classes_students(1)
        subject_name = self.renderer.get_subject_name(classes_students_record)
        self.assertEqual(subject_name, "Fisica")

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the class after running the tests.

        This method is a class method and is automatically called after all the tests in the class have been run. It is responsible for rolling back the database changes made during the tests and resetting the global variables.

        Parameters:
            cls (type): The class itself.

        Returns:
            None
        """
        cls.db.rollback()
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
