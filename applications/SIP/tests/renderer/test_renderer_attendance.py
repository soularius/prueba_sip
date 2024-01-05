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
        FakeGenerateController(cls.db).static_data_generate()
        FakeGenerateController(cls.db).index()
        current.db = cls.db
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.renderer = RendererAttendance(self.db)

    def test_render_view(self):
        self.request = Request({'wsgi.input': None, 'env': {'request_method': 'GET'}})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'attendance_view'

        from gluon.globals import current
        current.request = self.request
        # Recuperar los registros de asistencia y generar la tabla
        attendance = self.db.attendance(1)
        attendance_records = self.db(self.db.attendance).select()
        result = self.renderer.render_view(attendance_records)
        
        # Decodificar el resultado de XML a una cadena de caracteres
        result_str = result.xml().decode("utf-8")

        # Validar que la tabla contiene los datos correctos
        self.assertIn('Marta Salcedo', result_str)
        self.assertIn('A63', result_str)
        self.assertIn('Fisica', result_str)
        self.assertIn('<select', result_str)

    def test_get_student_name(self):
        students = self.db(self.db.students).select()
        # Prueba el método get_student_name
        classes_students_record = self.db.classes_students(1)
        student_name = self.renderer.get_student_name(classes_students_record)
        self.assertEqual(student_name, "Marta Salcedo")

    def test_get_salon_name(self):
        # Prueba el método get_salon_name
        classes_students_record = self.db.classes_students(1)
        salon_name = self.renderer.get_salon_name(classes_students_record)
        self.assertEqual(salon_name, "A63")

    def test_get_subject_name(self):
        # Prueba el método get_subject_name
        classes_students_record = self.db.classes_students(1)
        subject_name = self.renderer.get_subject_name(classes_students_record)
        self.assertEqual(subject_name, "Fisica")

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
