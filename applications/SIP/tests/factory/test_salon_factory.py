import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.salons import Salons
from applications.SIP.modules.utils.fake_data_salons_generator import FakeDataSalonGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.salon_factory import SalonFactory

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

class TestSalonFactory(unittest.TestCase):
        
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Salons(self.db).define_table()
        FakeDataSalonGenerator(self.db).generate_salons(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Inicializa el factory
        self.factory = SalonFactory(self.db)

    def test_create_salon(self):
        # Prueba la creación de un salón
        salon_data = {'name': 'A101', 'description': 'Math Class'}
        salon = self.factory.get_or_create_salon(salon_data)
        self.assertIn(salon.id, self.factory.cache)

    def test_get_salon(self):
        # Prueba la recuperación de un salón
        salon_data = {'name': 'B202', 'description': 'Physics Lab'}
        created_salon = self.factory.get_or_create_salon(salon_data)
        fetched_salon = self.factory.get_salon(created_salon.id)
        self.assertEqual(fetched_salon.id, created_salon.id)

    def test_list_salons(self):
        # Prueba la lista de salones
        salons = self.factory.list_salons()
        self.assertTrue(len(salons) > 0)

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
