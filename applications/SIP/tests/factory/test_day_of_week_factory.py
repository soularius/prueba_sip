import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.day_of_week import DayOfWeek
from applications.SIP.modules.utils.fake_data_day_of_week_generator import FakeDataDayOfWeekGenerator

from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.day_of_week_factory import DayOfWeekFactory

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

class TestDayOfWeekFactory(unittest.TestCase):
        
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        DayOfWeek(self.db).define_table()
        FakeDataDayOfWeekGenerator(self.db).generate_days_of_week()

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Inicializa el factory
        self.factory = DayOfWeekFactory(self.db)

    def test_create_day_of_week(self):
        # Prueba la creación de un día de la semana
        day_data = {'name': 'Monday'}
        day = self.factory.get_or_create_day_of_week(day_data)
        self.assertIn(day.id, self.factory.cache)

    def test_get_day_of_week(self):
        # Prueba la recuperación de un día de la semana
        day_data = {'name': 'Tuesday'}
        created_day = self.factory.get_or_create_day_of_week(day_data)
        fetched_day = self.factory.get_day_of_week(created_day.name)
        self.assertEqual(fetched_day.id, created_day.id)

    def test_list_days_of_week(self):
        # Prueba la lista de días de la semana
        days = self.factory.list_days_of_week()
        self.assertTrue(len(days) > 0)

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