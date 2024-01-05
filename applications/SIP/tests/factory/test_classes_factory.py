import unittest
from mock import Mock
from gluon.dal import DAL, Field
from gluon.globals import Request, Response, Session
from gluon import current

from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.classes_factory import ClassesFactory

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

class TestClassesFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the class for testing.

        This method is a class method and is called before any tests are run. It sets up the necessary database and defines the required tables for testing. The tables include 'Student', 'DayOfWeek', 'Salons', 'Schedules', 'Subjects', 'Teachers', 'Classes', 'ClassesStudents', and 'Attendance'. Additionally, it calls the 'index' method of the 'FakeGenerateController' class to generate fake data for testing. Finally, it sets the database connection for the current class to the created database.

        Parameters:
            cls (type): The class object.

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
        Set up the test case by initializing the necessary variables and objects.
        """
        from gluon.globals import current
        current.response = Response()

        self.factory = ClassesFactory(self.db)

    def test_create_class(self):
        """
        Test case for creating a class.

        This function tests the creation of a class by providing a class_data dictionary containing the necessary information for creating a class. The function calls the get_or_create_class method of the factory object and asserts that the created class object is present in the cache.

        Args:
            self: The test case object.

        Returns:
            None.
        """
        # Test creating a class
        class_data = {'code': 'CLS101', 'salon_id': 6, 'subject_id': 6, 'schedule_id' : 6, 'teacher_id': 6, 'day_of_week_id': 6}
        class_obj = self.factory.get_or_create_class(class_data)
        self.assertIn(class_obj.id, self.factory.cache)

    def test_read_class(self):
        """
        Test the read_class() method.

        This method tests the functionality of the read_class() method in the Factory class.
        It verifies that a class can be retrieved from the database using the provided class data.

        Parameters:
        - self: The instance of the test class.

        Returns:
        - None
        """
        # Recovery test for a class
        class_data = {'code': 'CLS101', 'salon_id': 6, 'subject_id': 6, 'schedule_id' : 6, 'teacher_id': 6, 'day_of_week_id': 6}
        created_class = self.factory.get_or_create_class(class_data)
        fetched_class = self.factory.get_class(created_class.id)
        self.assertEqual(fetched_class.id, created_class.id)

    def test_update_class(self):
        """
        Test updating a class.

        Parameters:
            self (TestClass): The instance of the TestClass.
        
        Returns:
            None.
        """
        # Test updating a class
        class_id = 2 # Assume an existing ID
        updated_data = {'code': 'CLS102'}
        self.factory.update_class(class_id, updated_data)
        updated_class = self.factory.get_class(class_id)
        self.assertEqual(updated_class.code, 'CLS102')

    def test_delete_class(self):
        """
        Test deleting a class.

        This function tests the functionality of deleting a class from the system.

        Parameters:
        - self: The instance of the test class.
        
        Returns:
        - None
        """
        # Test removing a class
        class_id = 4 # Assume an existing ID
        self.factory.delete_class(class_id)
        self.assertNotIn(class_id, self.factory.cache)

    def test_list_classes(self):
        """
        Test the list_classes method of the factory object.
        This method should return a list of classes.

        Parameters:
            self (TestClass): An instance of the TestClass.

        Returns:
            None
        """
        # Class listing test
        classes = self.factory.list_classes()
        self.assertTrue(len(classes) > 0)

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the class after running the test cases.

        There are no parameters for this method.

        This method does not return anything.

        This method rolls back any database transactions made during the test case.
        It also sets the request, response, session, and db objects in the current global context to None.
        """
        cls.db.rollback()
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
