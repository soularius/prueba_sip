import unittest
from mock import Mock
from gluon.globals import Request, Session, Storage
from applications.SIP.controllers.subjects_controller import SubjectsController

class TestSubjectsController(unittest.TestCase):

    def setUp(self):
        # Configura un entorno de prueba
        self.db = Mock()  # Utiliza un mock para la base de datos
        self.request = Request({})
        self.session = Session()
        self.response = Storage()
        self.response.flash = None

        # Simula SQLFORM con un mock que tiene un método grid
        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")

    def test_index(self):
        # Crea una instancia del controlador con el entorno de prueba
        controller = SubjectsController(self.db, self.SQLFORM)

        # Simula una petición al método index
        result = controller.index()

        # Verifica si se retorna el grid mockeado
        self.assertEqual(result, dict(grid="Mock Grid"))

if __name__ == '__main__':
    unittest.main()
