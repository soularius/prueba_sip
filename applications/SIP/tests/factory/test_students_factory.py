import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.student import Student
from applications.SIP.modules.utils.fake_data_student_generator import FakeDataStudentGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.students_factory import StudentFactory

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

class TestStudentFactory(unittest.TestCase):
        
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Student(self.db).define_table()
        FakeDataStudentGenerator(self.db).generate_students(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Inicializa el factory
        self.factory = StudentFactory(self.db)

    def test_create_student(self):
        # Prueba la creación de un estudiante
        student_data = {'name': 'John', 'lastname': 'Doe', 'email': 'john.doe@example.com', 'phone': '12345678'}
        student = self.factory.get_or_create_student(student_data)
        self.assertIn(student.id, self.factory.cache)

    def test_get_student(self):
        # Prueba la recuperación de un estudiante
        student_data = {'name': 'Jane', 'lastname': 'Doe', 'email': 'jane.doe@example.com', 'phone': '33345678'}
        created_student = self.factory.get_or_create_student(student_data)
        fetched_student = self.factory.get_student(created_student.id)
        self.assertEqual(fetched_student.id, created_student.id)

    def test_list_students(self):
        # Prueba la lista de estudiantes
        students = self.factory.list_students(1, 10)
        self.assertTrue(len(students) > 0)

    def tearDown(self):
        # Restablecer el estado de 'current' después de cada prueba
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
