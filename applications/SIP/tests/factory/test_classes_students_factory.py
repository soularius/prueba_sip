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

        self.factory = ClassesStudentsFactory(self.db)

    def test_create_classes_student(self):
        # Prueba de creación de una relación clase-estudiante
        classes_student_data = {'section_class': 'SEC101', 'classes_id': 2, 'student_id': 2}
        classes_student_obj = self.factory.get_or_create_classes_student(classes_student_data)
        self.assertIn(classes_student_obj.id, self.factory.cache)

    def test_read_classes_student(self):
        # Prueba de recuperación de una relación clase-estudiante
        classes_student_data = {'section_class': 'SEC102', 'classes_id': 3, 'student_id': 4}
        created_classes_student = self.factory.get_or_create_classes_student(classes_student_data)
        fetched_classes_student = self.factory.get_classes_student(created_classes_student.id)
        self.assertEqual(fetched_classes_student.id, created_classes_student.id)

    def test_update_classes_student(self):
        # Prueba de actualización de una relación clase-estudiante
        classes_student_id = 2 # Asume un ID existente
        updated_data = {'section_class': 'SEC106', 'classes_id': 5, 'student_id': 6}
        self.factory.update_classes_student(classes_student_id, updated_data)
        updated_classes_student = self.factory.get_classes_student(classes_student_id)
        self.assertEqual(updated_classes_student.section_class, 'SEC106')

    def test_delete_classes_student(self):
        # Prueba de eliminación de una relación clase-estudiante
        classes_student_id = 1 # Asume un ID existente
        self.factory.delete_classes_student(classes_student_id)
        self.assertNotIn(classes_student_id, self.factory.cache)

    def test_list_classes_students(self):
        # Prueba de listado de relaciones clase-estudiante
        classes_students = self.factory.list_classes_students()
        self.assertTrue(len(classes_students) > 0)

    @classmethod
    def tearDownClass(cls):
        cls.db.rollback()

if __name__ == '__main__':
    unittest.main()