import unittest
from mock import Mock
from gluon import DAL, URL
from gluon.globals import Request, Response, Session
from applications.SIP.controllers.students import api_create_student
from applications.SIP.controllers.students import api_list_student
from applications.SIP.controllers.students import api_get_student
from applications.SIP.controllers.students import api_update_student
from applications.SIP.controllers.students import api_delete_student
from applications.SIP.controllers.students import api_total_students


from applications.SIP.modules.models.student import Student
from applications.SIP.modules.utils.fake_data_student_generator import FakeDataStudentGenerator

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


class TestStudentsController(unittest.TestCase):
    def setUp(self):
        from gluon.globals import current
        current.response = Response()

        self.db = DAL('sqlite:memory:')

        Student(self.db).define_table()
        FakeDataStudentGenerator(self.db).generate_students(50)

        self.SQLFORM = Mock()
        self.SQLFORM.grid = Mock(return_value="Mock Grid")

    def test_api_create_student(self):
        # Configurar el objeto request
        env = {'request_method': 'POST', "PATH_INFO": '/SIP/students/api_create_student'}
        self.request = Request(env)
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_create_student'
        self.request._post_vars = {
            'name': "John",
            'lastname': "Doe",
            'phone': "3239940542",
            'email': "johndoe@example.com"
        }
        self.request.is_restful = True
        
        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_create_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)

        self.assertEqual(response['http_status'], 201)  # Asumiendo que devuelves 201 en caso de éxito
        self.assertIn('success', response['status'])

    def test_api_list_student(self):
        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_list_student'
        self.request.vars = {'page': 1, 'page_size': 10}

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_list_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)  # Asumiendo que devuelves 200 en caso de éxito

    def test_api_get_student(self):
        # Asegúrate de tener un registro de estudiante válido para probar
        student_id = '1'  # Reemplaza con un ID válido si es necesario

        self.request = Request(env={'request_method': 'GET'})
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_get_student'
        self.request.args = [student_id]

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_get_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)

    def test_api_update_student(self):
        student_id = '3'  # Reemplaza con un ID válido si es necesario

        self.request = Request(env={'request_method': 'PUT'})
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_update_student'
        self.request.args = [student_id]
        self.request._post_vars = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
        
        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_update_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)

    def test_api_delete_student(self):
        student_id = '1'

        self.request = Request(env={'request_method': 'DELETE'})
        self.request.application = 'SIP'
        self.request.controller = 'students'
        self.request.function = 'api_delete_student'
        self.request.args = [student_id]

        from gluon.globals import current
        current.request = self.request
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_delete_student()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
    
    def test_api_total_students(self):
        from gluon.globals import current
        current.db = self.db

        from gluon.http import HTTP
        try:
            response = api_total_students()
        except HTTP as http_response:
            response = http_response.body
        if isinstance(response, str):
            import json
            response = json.loads(response)
        self.assertEqual(response['http_status'], 200)
        # Aquí puedes hacer más aserciones para comprobar la respuesta


    def tearDown(self):
        # Restablecer el estado de 'current' después de cada prueba
        from gluon.globals import current
        current.request = None
        current.response = None
        current.session = None
        current.db = None

if __name__ == '__main__':
    unittest.main()