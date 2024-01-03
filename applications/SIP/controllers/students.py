from applications.SIP.controllers.students_controller import StudentsController
from applications.SIP.modules.services.api_services.api_students import APIStudent

def index():
    controller = StudentsController(db, SQLFORM)
    return controller.index()

def students_register_ts():
    return dict(tittle="Registro de Estudiante")

def api_list_student():
    page = int(request.vars.page or 1)
    page_size = int(request.vars.page_size or 10)
    api_student = APIStudent(db)
    students = api_student.list_student(page, page_size)
    return response.json(students)

def api_get_student():
    student_id = request.args(0)  # Obtener el ID del estudiante de los argumentos URL
    if student_id:
        api_student = APIStudent(db)
        result = api_student.get_student(student_id)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'No student ID provided'})

def api_create_student():
    if request.env.request_method == 'POST':
        api_student = APIStudent(db)
        result = api_student.create_student(request.post_vars)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request method'})

def api_update_student():
    student_id = request.args(0)  # Obtener el ID del estudiante de los argumentos URL
    if student_id and request.env.request_method in ['PUT', 'POST']:
        api_student = APIStudent(db)
        student_data = request.post_vars
        result = api_student.update_student(student_id, student_data)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request'})

def api_delete_student():
    student_id = request.args(0)  # Obtener el ID del estudiante de los argumentos URL
    if student_id and request.env.request_method == 'DELETE':
        api_student = APIStudent(db)
        result = api_student.delete_student(student_id)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request'})