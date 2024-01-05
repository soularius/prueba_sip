import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.teachers import Teachers
from applications.SIP.modules.utils.fake_data_teacher_generator import FakeDataTeacherGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.teacher_factory import TeacherFactory

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

class TestTeacherFactory(unittest.TestCase):
        
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Teachers(self.db).define_table()
        FakeDataTeacherGenerator(self.db).generate_teachers(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Inicializa el factory
        self.factory = TeacherFactory(self.db)

    def test_create_teacher(self):
        # Prueba la creación de un profesor
        teacher_data = {'name': 'John', 'lastname': 'Doe', 'phone': '123456789', 'email': 'johndoe@example.com'}
        teacher = self.factory.get_or_create_teacher(teacher_data)
        self.assertIn(teacher.id, self.factory.cache)

    def test_get_teacher(self):
        # Prueba la recuperación de un profesor
        teacher_data = {'name': 'Jane', 'lastname': 'Smith', 'phone': '987654321', 'email': 'janesmith@example.com'}
        created_teacher = self.factory.get_or_create_teacher(teacher_data)
        fetched_teacher = self.factory.get_teacher(created_teacher.id)
        self.assertEqual(fetched_teacher.id, created_teacher.id)

    def test_list_teachers(self):
        # Prueba la lista de profesores
        teachers = self.factory.list_teachers()
        self.assertTrue(len(teachers) > 0)

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

