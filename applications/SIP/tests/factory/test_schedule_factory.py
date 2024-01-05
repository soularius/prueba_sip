import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session

from applications.SIP.modules.models.schedules import Schedules
from applications.SIP.modules.utils.fake_data_schedules_generator import FakeDataScheduleGenerator
from applications.SIP.modules.factory.singleton_meta import SingletonMeta
from applications.SIP.modules.factory.schedule_factory import ScheduleFactory

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

class TestScheduleFactory(unittest.TestCase):
        
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Schedules(self.db).define_table()
        FakeDataScheduleGenerator(self.db).generate_schedules(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")
        # Inicializa el factory
        self.factory = ScheduleFactory(self.db)

    def test_create_schedule(self):
        # Prueba la creación de un horario
        schedule_data = {'block_start': '08:00', 'block_end': '10:00'}
        schedule = self.factory.get_or_create_schedule(schedule_data)
        self.assertIn(schedule.id, self.factory.cache)

    def test_get_schedule(self):
        # Prueba la recuperación de un horario
        schedule_data = {'block_start': '10:00', 'block_end': '12:00'}
        created_schedule = self.factory.get_or_create_schedule(schedule_data)
        fetched_schedule = self.factory.get_schedule(created_schedule.id)
        self.assertEqual(fetched_schedule.id, created_schedule.id)

    def test_list_schedules(self):
        # Prueba la lista de horarios
        schedules = self.factory.list_schedules()
        self.assertTrue(len(schedules) > 0)

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
