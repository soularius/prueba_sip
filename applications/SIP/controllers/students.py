from applications.SIP.controllers.students_controller import StudentsController
from applications.SIP.modules.services.api_services.api_students import APIStudent
from gluon import current
from gluon.html import URL

def index():
    db = current.db
    controller = StudentsController(db, SQLFORM)
    return controller.index()

def students_register_ts():
    return dict(tittle="Registro de Estudiante")

def students_list_ts():
    return dict(tittle="Listado de Estudiantes")

def students_view_ts():
    db = current.db
    request = current.request
    student_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    return dict(tittle="Detalle de Estudiante", student_id=student_id)

def students_edit_ts():
    db = current.db
    request = current.request
    student_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    return dict(tittle="Editar Estudiante", student_id=student_id)

def api_list_student():
    db = current.db
    request = current.request
    response = current.response
    page = int(request.vars.page or 1)
    page_size = int(request.vars.page_size or 10)
    api_student = APIStudent(db)
    students = api_student.list_student(page, page_size)
    return response.json(students)

def api_get_student():
    db = current.db
    request = current.request
    response = current.response
    student_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    if student_id:
        api_student = APIStudent(db)
        result = api_student.get_student(student_id)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'No student ID provided', 'http_status': 404})

def api_create_student():
    db = current.db
    request = current.request
    response = current.response
    if request.env.request_method == 'POST':
        api_student = APIStudent(db)
        result = api_student.create_student(request.post_vars)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request method', 'http_status': 500})

def api_update_student():
    db = current.db
    request = current.request
    response = current.response
    student_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    if student_id and request.env.request_method in ['PUT', 'POST']:
        api_student = APIStudent(db)
        student_data = request.post_vars
        result = api_student.update_student(student_id, student_data)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request method', 'http_status': 500})

def api_delete_student():
    db = current.db
    request = current.request
    response = current.response
    student_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    if student_id and request.env.request_method == 'DELETE':
        api_student = APIStudent(db)
        result = api_student.delete_student(student_id)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request method', 'http_status': 500})
    
def api_total_students():
    db = current.db
    response = current.response
    api_student = APIStudent(db)
    result = api_student.get_total_students()
    return response.json(result)