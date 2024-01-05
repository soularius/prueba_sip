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

        self.factory = AttendanceFactory(self.db)

    def test_create_attendance(self):
        # Crear una asistencia y comprobar que se añade a la caché
        attendance_data = {'classes_students_id': '2', 'date_class': '2023-01-01', 'status': '1', 'note': 'Loremp'}
        attendance = self.factory.get_or_create_attendance(attendance_data)
        self.assertIn(attendance.id, self.factory.cache)

    def test_read_attendance(self):
        # Crear y luego recuperar una asistencia
        attendance_data = {'classes_students_id': '2', 'date_class': '2023-01-01', 'status': '1', 'note': 'Loremp'}
        created_attendance = self.factory.get_or_create_attendance(attendance_data)
        fetched_attendance = self.factory.get_attendance(created_attendance.id)
        self.assertEqual(fetched_attendance.id, created_attendance.id)

    def test_update_attendance(self):
        # Actualizar una asistencia
        attendance_id = 2
        updated_data = {'classes_students_id': '2', 'date_class': '2023-01-01', 'status': '1', 'note': 'Loremp'}
        self.factory.update_attendance(attendance_id, updated_data)
        updated_attendance = self.factory.get_attendance(attendance_id)
        self.assertEqual(updated_attendance.date_class, '2023-01-01')

    def test_delete_attendance(self):
        # Eliminar una asistencia
        attendance_id = 1
        self.factory.delete_attendance(attendance_id)
        self.assertNotIn(attendance_id, self.factory.cache)

    def test_list_attendances(self):
        # Listar asistencias
        attendances = self.factory.list_attendances(1, 10)
        self.assertTrue(len(attendances) > 0)

    @classmethod
    def tearDownClass(cls):
        cls.db.rollback()
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
