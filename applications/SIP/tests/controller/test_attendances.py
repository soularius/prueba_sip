import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session
from applications.SIP.controllers.attendances import attendance_view
from applications.SIP.controllers.attendances import attendance_update
from applications.SIP.controllers.attendances import api_create_attendance
from applications.SIP.controllers.attendances import api_list_attendance
from applications.SIP.controllers.attendances import api_get_attendance
from applications.SIP.controllers.attendances import api_update_attendance
from applications.SIP.controllers.attendances import api_delete_attendance

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
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Student(self.db).define_table()
        DayOfWeek(self.db).define_table()
        Salons(self.db).define_table()
        Schedules(self.db).define_table()
        Subjects(self.db).define_table()
        Teachers(self.db).define_table()
        Classes(self.db).define_table()
        ClassesStudents(self.db).define_table()
        Attendance(self.db).define_table()
        controller = FakeGenerateController(self.db).index()

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")

    def test_attendance_view(self):
        # Configurar el objeto request
        self.request = Request({'wsgi.input': None, 'env': {'request_method': 'GET'}})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'attendance_view'

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        # Obtener un registro de prueba
        record = self.db.attendance(1)
        # Construir la URL
        constructed_url = URL('SIP', 'attendances', 'attendance_update', args=[record.id], extension='json')
        self.assertEqual(constructed_url, '/SIP/attendances/attendance_update.json/1')
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
        current.db = self.db

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
        attendance_id = '1'  # Reemplaza con un ID válido si es necesario

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
        attendance_id = "1"

        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'attendances'
        self.request.function = 'api_get_attendance'
        self.request.args = [attendance_id]

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

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

    def tearDown(self):
        # Restablecer el estado de 'current' después de cada prueba
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()
