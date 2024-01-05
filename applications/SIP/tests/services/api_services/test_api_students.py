import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.student import Student
from applications.SIP.modules.utils.fake_data_student_generator import FakeDataStudentGenerator

from applications.SIP.modules.factory.students_factory import StudentFactory
from applications.SIP.modules.services.api_services.api_students import APIStudent

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

class TestAPIStudent(unittest.TestCase):
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Student(self.db).define_table()
        FakeDataStudentGenerator(self.db).generate_students(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        
        # Aquí debes definir las tablas necesarias para tus pruebas, como Student, etc.
        self.api_student = APIStudent(self.db)

    def test_create_student(self):
        # Prueba la creación de un estudiante
        student_data = {'name': 'Juan', 'lastname': 'Pérez', 'email': 'juan@example.com', 'phone': '1234567890'}
        response = self.api_student.create_student(student_data)
        self.assertEqual(response['http_status'], 201)
        self.assertEqual(response['status'], 'success')

    def test_list_student(self):
        # Prueba el listado de estudiantes
        response = self.api_student.list_student()
        self.assertEqual(response['http_status'], 200)
        self.assertIsInstance(response['students'], list)

    def test_get_student(self):
        # Prueba obtener un estudiante específico
        student_id = 1  # Asegúrate de que este ID exista
        response = self.api_student.get_student(student_id)
        self.assertEqual(response['http_status'], 200)

    def test_update_student(self):
        # Prueba actualizar un estudiante
        student_id = 1  # Asegúrate de que este ID exista
        student_data = {'name': 'Ana'}  # Actualización de datos
        response = self.api_student.update_student(student_id, student_data)
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    def test_delete_student(self):
        # Prueba eliminar un estudiante
        student_id = 1  # Asegúrate de que este ID exista
        response = self.api_student.delete_student(student_id)
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    def test_get_total_students(self):
        # Prueba obtener el total de estudiantes
        response = self.api_student.get_total_students()
        self.assertEqual(response['http_status'], 200)
        self.assertEqual(response['status'], 'success')

    def tearDown(self):
        # Limpia el entorno después de cada prueba
        self.db.close()

if __name__ == '__main__':
    unittest.main()