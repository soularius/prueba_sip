import unittest
from mock import Mock
from gluon.dal import DAL, Field
from gluon.globals import Request, Response, Session
from gluon import current

from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.classes_students_factory import ClassesStudentsFactory

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

class TestClassesStudentsFactory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the class for testing.

        This method is a class method and is used to set up the necessary resources for testing the class. It creates an in-memory SQLite database and defines tables for the Student, DayOfWeek, Salons, Schedules, Subjects, Teachers, Classes, ClassesStudents, Attendance, and FakeGenerateController models. It also sets the current database to the created database.

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
        Set up the necessary environment for the test case.

        This function initializes the current response object and
        creates an instance of the ClassesStudentsFactory class
        using the database connection.

        Parameters:
        - self: The instance of the test case class.

        Return:
        - None
        """
        from gluon.globals import current
        current.response = Response()

        self.factory = ClassesStudentsFactory(self.db)

    def test_create_classes_student(self):
        """
        Test the creation of a class-student relationship.

        This function creates a class-student relationship using the provided section_class, classes_id, and student_id.
        It then checks that the created classes_student_obj has been added to the factory cache.

        Parameters:
            self (TestClass): The instance of the TestClass that the test is being run on.

        Returns:
            None
        """
        # Test for creating a class-student relationship
        classes_student_data = {'section_class': 'SEC101', 'classes_id': 6, 'student_id': 6}
        classes_student_obj = self.factory.get_or_create_classes_student(classes_student_data)
        self.assertIn(classes_student_obj.id, self.factory.cache)

    def test_read_classes_student(self):
        """
        Test the functionality of reading a relationship between a class and a student.

        Args:
            self (TestCase): The current instance of the test case.

        Returns:
            None
        """
        # Test of recovery of a class-student relationship
        classes_student_data = {'section_class': 'SEC102', 'classes_id': 6, 'student_id': 6}
        created_classes_student = self.factory.get_or_create_classes_student(classes_student_data)
        fetched_classes_student = self.factory.get_classes_student(created_classes_student.id)
        self.assertEqual(fetched_classes_student.id, created_classes_student.id)

    def test_update_classes_student(self):
        """
        Updates a class-student relationship.

        Args:
            classes_student_id (int): The ID of the class-student relationship to be updated.
            updated_data (dict): A dictionary containing the updated data for the relationship.
                - section_class (str): The updated section class.
                - classes_id (int): The updated class ID.
                - student_id (int): The updated student ID.

        Returns:
            None
        """
        # Test updating a class-student relationship
        classes_student_id = 2 # Assume an existing ID
        updated_data = {'section_class': 'SEC106', 'classes_id': 6, 'student_id': 6}
        self.factory.update_classes_student(classes_student_id, updated_data)
        updated_classes_student = self.factory.get_classes_student(classes_student_id)
        self.assertEqual(updated_classes_student.section_class, 'SEC106')

    def test_delete_classes_student(self):
        """
        Test the delete_classes_student method.

        Parameters:
            self (TestClass): The instance of the test class.
        
        Returns:
            None
        """
        # Test for removing a class-student relationship
        classes_student_id = 4 # Assume an existing ID
        self.factory.delete_classes_student(classes_student_id)
        self.assertNotIn(classes_student_id, self.factory.cache)

    def test_list_classes_students(self):
        """
        Test the list of class-student relationships.

        This function tests the functionality of the `list_classes_students` method
        in the `factory` object. It retrieves a list of class-student relationships
        and asserts that the length of the list is greater than 0.

        Parameters:
            self (TestCase): The current test case object.

        Returns:
            None
        """
        # Class-student relationship listing test
        classes_students = self.factory.list_classes_students()
        self.assertTrue(len(classes_students) > 0)

    @classmethod
    def tearDownClass(cls):
        """
        Tears down the entire class by rolling back the database transaction and resetting the current request, response, session, and db objects.

        :param cls: The class object.
        :type cls: Class
        :return: None
        """
        cls.db.rollback()
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()