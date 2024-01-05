import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session
from applications.SIP.controllers.attendances import *

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

class TestAttendancesController(unittest.TestCase):

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

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")

    def test_attendance_view(self):
        record_id = '2'
        # Configurar el objeto request
        self.request = Request({'wsgi.input': None, 'env': {'request_method': 'GET'}})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'attendance_view'

        from gluon.globals import current
        current.request = self.request

        # Obtener un registro de prueba
        record = self.db.attendance(record_id)
        # Construir la URL
        constructed_url = URL('SIP', 'attendances', 'attendance_update', args=[record.id], extension='json')
        self.assertEqual(constructed_url, f'/SIP/attendances/attendance_update.json/{record_id}')
        result = attendance_view()
    
    def test_attendance_update(self):
        # Crear un registro de asistencia para la prueba
        record_id = '3'
        updated_record = self.db.attendance(record_id)
        self.db.commit()

        # Configurar el objeto request para una actualización exitosa
        new_status = '1'
        self.request = Request({'wsgi.input': None, 'env': {'request_method': 'GET'}})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'attendance_update'
        self.request.args = [record_id]  # ID del registro a actualizar
        self.request._post_vars = {f'status_{record_id}': new_status}  # Nuevo estado

        from gluon.globals import current
        current.request = self.request

        # Llamar a la función de actualización
        response = attendance_update()

        # Verificar que el estado se haya actualizado correctamente
        updated_record = self.db.attendance(record_id)
        self.assertEqual(updated_record.status, int(new_status))

    def test_api_create_attendance(self):
        # Configurar el objeto request
        env = {'request_method': 'POST', "PATH_INFO": '/SIP/attendances/api_create_attendance'}
        self.request = Request(env)
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_create_attendance'
        self.request._post_vars = {   'classes_students_id': 1, 
                                'date_class': "2023-10-27",
                                'status': 1,
                                'note': "Test note"
                            }
        self.request.is_restful = True
        
        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_create_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 201)
        self.assertIn('success', response['status']) 

    def test_api_update_attendance(self):
        attendance_id = '2'  # Reemplaza con un ID válido si es necesario

        env = {'request_method': 'PUT', "PATH_INFO": '/SIP/attendances/api_update_attendance'}
        self.request = Request(env)
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_update_attendance'
        self.request.args = [attendance_id]
        self.request._post_vars = {'status': 0, 'note': 'Updated note'}
        self.request.is_restful = True

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        # Ejecutar la prueba
        from gluon.http import HTTP
        try:
            response = api_update_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
    
    def test_api_list_attendance(self):
        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_list_attendance'
        self.request.vars = {'page': 1, 'page_size': 10}

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_list_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
    
    def test_api_get_attendance(self):
        # Asegúrate de tener un registro de asistencia válido para probar
        attendance_id = '3'

        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_get_attendance'
        self.request.args = [attendance_id]
        
        from gluon.globals import current
        current.request = self.request

        from gluon.http import HTTP
        try:
            response = api_get_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
   
    def test_api_delete_attendance(self):
        attendance_id = '1'  # Reemplaza con un ID válido si es necesario

        self.request = Request(env={'request_method': 'DELETE'})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_delete_attendance'
        self.request.args = [attendance_id]

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_delete_attendance()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)

    @classmethod
    def tearDownClass(cls):
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
