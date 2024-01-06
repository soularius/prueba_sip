from applications.SIP.controllers.attendances_controller import AttendancesController
from applications.SIP.modules.renderer.renderer_attendance import RendererAttendance
from applications.SIP.modules.services.api_services.api_attendances import APIAttendance
from applications.SIP.modules.factory.attendance_factory import AttendanceFactory
from gluon import current
from gluon.html import URL
import json

def index():
    """
    Return the index page of the application.
    This function initializes the database connection, creates an instance of the AttendancesController class, 
    and calls the index() method of the controller to retrieve the index page data.
    
    :return: The index page data.
    :rtype: Any
    """
    db = current.db
    controller = AttendancesController(db, SQLFORM)
    return controller.index()

def attendance_view():
    """
    Function to display the attendance view.

    This function retrieves the necessary data to display the attendance records
    for a specific page. The page number is obtained from the URL arguments, and
    if no page number is provided, the default page is set to 1. The number of
    items to display per page is set to 10.

    The function calculates the total number of pages based on the total number
    of attendance records in the database and the number of items per page. If
    there are no records, a flash message is set and a dictionary is returned
    with the table set to "Sin registros existentes" (No existing records),
    items_per_page, page, and total_pages.

    If the requested page number exceeds the total number of pages, the user is
    redirected to the last available page.

    The function calls the `list_attendances()` method of the `AttendanceFactory`
    class to retrieve the attendance records for the specified page. The returned
    records are then passed to the `RendererAttendance` class to generate the
    HTML table representation.

    The function finally returns a dictionary containing the generated attendance
    table, the number of items per page, the current page number, and the total
    number of pages.

    :return: A dictionary containing the attendance table, items per page, page
             number, and total number of pages.
    :rtype: dict
    """
    request = current.request
    response = current.response
    page = int(request.args[0]) if request.args and request.args[0].isdigit() else 1
    items_per_page = 10
    total_pages = 0

    attendance_factory = AttendanceFactory(current.db)
    total_records = current.db(current.db.attendance).count()  # Se mantiene para contar los registros
    total_pages = (total_records // items_per_page) + (1 if total_records % items_per_page else 0)

    if total_records == 0:
        response.flash = "No hay registros de asistencia disponibles."
        return dict(table="Sin registros existentes", items_per_page=items_per_page, page=page, total_pages=total_pages)

    if page > total_pages:
        redirect(URL('attendance_view', args=[total_pages if total_pages > 0 else 1]))

    attendance_records = attendance_factory.list_attendances(page, items_per_page)

    renderer = RendererAttendance(current.db)
    attendance_table = renderer.render_view(attendance_records)

    return dict(table=attendance_table, items_per_page=items_per_page, page=page, total_pages=total_pages)

def attendance_update():
    """
    Update the attendance record with the given record ID and new status.

    Parameters:
    - None

    Returns:
    - JSON response
    """
    request = current.request
    response = current.response

    # Asegúrate de que se proporciona un record_id válido
    try:
        record_id = int(request.args[0])
    except (IndexError, ValueError):
        return json.dumps({'status': 'error', 'message': 'ID de registro inválido'})

    new_status_key = f'status_{record_id}'
    new_status = request.vars.get(new_status_key)

    attendance_factory = AttendanceFactory(current.db)

    if record_id and new_status is not None:
        updated_attendance = attendance_factory.update_attendance(record_id, {'status': new_status})
        if updated_attendance:
            response.flash = "Attendance updated successfully AJAX"
            return json.dumps({'status': 'success', 'message': response.flash, 'http_status': 200})
        else:
            response.flash = "Error updated attendance AJAX"
            return json.dumps({'status': 'error', 'message': response.flash, 'http_status': 500})
    else:
        response.flash = "Error updated attendance AJAX"
        return json.dumps({'status': 'error', 'message': response.flash, 'http_status': 500})

def api_list_attendance():
    """
    This function lists the attendance records from the API.

    Parameters:
        None

    Returns:
        A JSON response containing the attendance records.
    """
    db = current.db
    request = current.request
    response = current.response
    page = int(request.vars.page or 1)
    page_size = int(request.vars.page_size or 10)
    api_attendance = APIAttendance(db)
    attendances = api_attendance.list_attendance(page, page_size)
    return response.json(attendances)

def api_get_attendance():
    """
    Retrieves the attendance record for a specific attendance ID.

    :return: A JSON response containing the attendance record.
    :rtype: dict
    """
    db = current.db
    request = current.request
    response = current.response
    attendance_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    if attendance_id:
        api_attendance = APIAttendance(db)
        result = api_attendance.get_attendance(attendance_id)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'No student ID provided', 'http_status': 404})

def api_create_attendance():
    """
    Create attendance using the API.

    This function creates attendance by processing a POST request. It receives the attendance data in the request body and uses the `APIAttendance` class to create the attendance record in the database.

    Parameters:
    - None

    Returns:
    - JSON response: The attendance creation result in JSON format. If the request method is not POST, it returns a JSON response with an error message and an HTTP status code of 500.
    """
    db = current.db
    request = current.request
    response = current.response
    if request.env.request_method == 'POST':
        api_attendance = APIAttendance(db)
        result = api_attendance.create_attendance(request.post_vars)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request method', 'http_status': 500})

def api_update_attendance():
    """
    Updates the attendance record in the API.

    Parameters:
        None

    Returns:
        If the attendance ID is provided and the request method is 'PUT' or 'POST',
        the function updates the attendance record with the given ID using the
        request post variables and returns the updated record as a JSON response.
        If the attendance ID or the request method is invalid, the function returns
        a JSON response with an error message and a status code of 500.
    """
    db = current.db
    request = current.request
    response = current.response
    attendance_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    if attendance_id and request.env.request_method in ['PUT', 'POST']:
        api_attendance = APIAttendance(db)
        result = api_attendance.get_attendance(attendance_id)
        result = api_attendance.update_attendance(attendance_id, request.post_vars)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request method', 'http_status': 500})

def api_delete_attendance():
    """
    Deletes an attendance record from the database.

    Parameters:
    - None

    Returns:
    - If the attendance record is successfully deleted, the function returns a JSON response containing the result.
    - If the attendance ID is not provided or the request method is not 'DELETE', the function returns a JSON response with an error message.
    """
    db = current.db
    request = current.request
    response = current.response
    attendance_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    if attendance_id and request.env.request_method == 'DELETE':
        api_attendance = APIAttendance(db)
        result = api_attendance.delete_attendance(attendance_id)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request method', 'http_status': 500})