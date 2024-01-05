import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.subjects import Subjects
from applications.SIP.modules.utils.fake_data_subjects_generator import FakeDataSubjectGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.subject_factory import SubjectFactory

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

class TestSubjectFactory(unittest.TestCase):
        
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Subjects(self.db).define_table()
        FakeDataSubjectGenerator(self.db).generate_subjects(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Inicializa el factory
        self.factory = SubjectFactory(self.db)

    def test_create_subject(self):
        # Prueba la creación de una materia
        subject_data = {'name': 'Math', 'description': 'Mathematics subject'}
        subject = self.factory.get_or_create_subject(subject_data)
        self.assertIn(subject.id, self.factory.cache)

    def test_get_subject(self):
        # Prueba la recuperación de una materia
        subject_data = {'name': 'Physics', 'description': 'Physics subject'}
        created_subject = self.factory.get_or_create_subject(subject_data)
        fetched_subject = self.factory.get_subject(created_subject.id)
        self.assertEqual(fetched_subject.id, created_subject.id)

    def test_list_subjects(self):
        # Prueba la lista de materias
        subjects = self.factory.list_subjects()
        self.assertTrue(len(subjects) > 0)

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
