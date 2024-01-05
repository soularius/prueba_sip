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

        # Aquí debes definir las tablas necesarias para tus pruebas, como Attendance, etc.
        self.api_attendance = APIAttendance(self.db)

    def test_create_attendance(self):
        # Prueba la creación de una asistencia
        attendance_data = {'classes_students_id': 1, 'date_class': '2023-01-01', 'status': 1, 'note': 'Present'}
        response = self.api_attendance.create_attendance(attendance_data)
        self.assertEqual(response['http_status'], 201)
        self.assertEqual(response['status'], 'success')

    def test_list_attendance(self):
        # Prueba el listado de asistencias
        response = self.api_attendance.list_attendance()
        self.assertEqual(response['http_status'], 200)
        self.assertIsInstance(response['attendances'], list)

    def test_get_attendance(self):
        # Prueba obtener una asistencia específica
        attendance_id = 1  # Asegúrate de que este ID exista
        response = self.api_attendance.get_attendance(attendance_id)
        self.assertEqual(response['http_status'], 200)

    def test_update_attendance(self):
        # Prueba actualizar una asistencia
        attendance_id = 1  # Asegúrate de que este ID exista
        attendance_data = {'status': 0}  # Actualización de datos
        response = self.api_attendance.update_attendance(attendance_id, attendance_data)
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    def test_delete_attendance(self):
        # Prueba eliminar una asistencia
        attendance_id = 2  # Asegúrate de que este ID exista
        response = self.api_attendance.delete_attendance(attendance_id)
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    @classmethod
    def tearDownClass(cls):
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
