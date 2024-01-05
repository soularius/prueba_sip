from applications.SIP.controllers.students_controller import StudentsController
from applications.SIP.modules.services.api_services.api_students import APIStudent
from gluon import current
from gluon.html import URL

def index():
    """
    This function returns the index page of the application.

    Parameters:
        None

    Returns:
        The index page of the application.

    """
    db = current.db
    controller = StudentsController(db, SQLFORM)
    return controller.index()

def students_register_ts():
    """
    Generates a function comment for the given function body in a markdown code block with the correct language syntax.
    
    Returns:
        str: The function comment for the given function body.
    """
    return dict(tittle="Registro de Estudiante")

def students_list_ts():
    """
    Generate the function comment for the given function body in a markdown code block with the correct language syntax.

    Returns:
        dict: A dictionary with the title "Listado de Estudiantes".

    """
    return dict(tittle="Listado de Estudiantes")

def students_view_ts():
    """
    Return a dictionary containing the title of the student view and the student ID.

    Parameters:
        None

    Returns:
        dict: A dictionary with the following key-value pairs:
            - 'title': The title of the student view (str).
            - 'student_id': The ID of the student (int).

    Example:
        >>> students_view_ts()
        {'title': 'Detalle de Estudiante', 'student_id': 0}
    """
    db = current.db
    request = current.request
    student_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    return dict(tittle="Detalle de Estudiante", student_id=student_id)

def students_edit_ts():
    """
    Edit a student's information.

    Parameters:
        None

    Returns:
        dict: A dictionary containing the title of the page and the student ID to edit.
    """
    db = current.db
    request = current.request
    student_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    return dict(tittle="Editar Estudiante", student_id=student_id)

def api_list_student():
    """
    A function that lists students from the API.

    Parameters:
        None.

    Returns:
        A JSON response containing the list of students.
    """
    db = current.db
    request = current.request
    response = current.response
    page = int(request.vars.page or 1)
    page_size = int(request.vars.page_size or 50)
    api_student = APIStudent(db)
    students = api_student.list_student(page, page_size)
    return response.json(students)

def api_get_student():
    """
    Retrieves a student from the database based on the provided student ID.

    Parameters:
        None.

    Returns:
        If the student ID is provided and valid, returns a JSON response containing the student information.
        If the student ID is not provided or invalid, returns a JSON response with an error message and HTTP status code 404.
    """
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
    """
    Create a new student record in the API.

    This function creates a new student record in the API database using the provided request data.
    
    Parameters:
    None
    
    Returns:
    - If the request method is POST:
        - A JSON response containing the result of creating the student record.
    - If the request method is not POST:
        - A JSON response indicating an error with the request method.

    Example Usage:
    ```
    response = api_create_student()
    print(response)
    ```
    """
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
    """
    Updates a student's information in the API.

    Parameters:
        None

    Returns:
        - If the student ID exists and the request method is either PUT or POST:
            - A JSON response with the result of updating the student's information.
        - If the student ID does not exist or the request method is not PUT or POST:
            - A JSON response with an error message and HTTP status code 500.
    """
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
    """
    Delete a student from the database based on the student ID.

    Parameters:
        None

    Returns:
        If the request is valid and the student is successfully deleted, returns a JSON response with the result.
        If the request is invalid or the student cannot be deleted, returns a JSON response with an error message.

    Raises:
        None
    """
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
    """
    Retrieves the total number of students from the database using the APIStudent class.

    Returns:
        dict: A JSON response containing the total number of students.
    """
    db = current.db
    response = current.response
    api_student = APIStudent(db)
    result = api_student.get_total_students()
    return response.json(result)