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

        self.factory = ClassesFactory(self.db)

    def test_create_class(self):
        # Prueba de creación de una clase
        class_data = {'code': 'CLS101', 'salon_id': 1, 'subject_id': 1, 'schedule_id' : 1, 'teacher_id': 1, 'day_of_week_id': 1}
        class_obj = self.factory.get_or_create_class(class_data)
        self.assertIn(class_obj.id, self.factory.cache)

    def test_read_class(self):
        # Prueba de recuperación de una clase
        class_data = {'code': 'CLS101', 'salon_id': 1, 'subject_id': 1, 'schedule_id' : 1, 'teacher_id': 1, 'day_of_week_id': 1}
        created_class = self.factory.get_or_create_class(class_data)
        fetched_class = self.factory.get_class(created_class.id)
        self.assertEqual(fetched_class.id, created_class.id)

    def test_update_class(self):
        # Prueba de actualización de una clase
        class_id = 2 # Asume un ID existente
        updated_data = {'code': 'CLS102'}
        self.factory.update_class(class_id, updated_data)
        updated_class = self.factory.get_class(class_id)
        self.assertEqual(updated_class.code, 'CLS102')

    def test_delete_class(self):
        # Prueba de eliminación de una clase
        class_id = 1 # Asume un ID existente
        self.factory.delete_class(class_id)
        self.assertNotIn(class_id, self.factory.cache)

    def test_list_classes(self):
        # Prueba de listado de clases
        classes = self.factory.list_classes()
        self.assertTrue(len(classes) > 0)

    @classmethod
    def tearDownClass(cls):
        cls.db.rollback()

if __name__ == '__main__':
    unittest.main()
