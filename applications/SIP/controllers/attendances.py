from applications.SIP.controllers.attendances_controller import AttendancesController
from applications.SIP.modules.renderer.renderer_attendance import RendererAttendance
from applications.SIP.modules.services.api_services.api_attendances import APIAttendance
from applications.SIP.modules.factory.attendance_factory import AttendanceFactory
from gluon import current
from gluon.html import URL

def index():
    db = current.db
    controller = AttendancesController(db, SQLFORM)
    return controller.index()

def attendance_view():
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
    request = current.request
    response = current.response
    record_id = int(request.args[0]) if request.args and request.args[0].isdigit() else 0
    new_status_key = f'status_{record_id}'
    new_status = request.vars.get(new_status_key)

    attendance_factory = AttendanceFactory(current.db)

    if record_id and new_status is not None:
        updated_attendance = attendance_factory.update_attendance(record_id, {'status': new_status})
        if updated_attendance:
            response.flash = "Estatus actualizado."
        else:
            response.flash = "Error al actualizar."
    else:
        response.flash = "Error al actualizar."
    return dict()

def api_list_attendance():
    db = current.db
    request = current.request
    response = current.response
    page = int(request.vars.page or 1)
    page_size = int(request.vars.page_size or 10)
    api_attendance = APIAttendance(db)
    attendances = api_attendance.list_attendance(page, page_size)
    return response.json(attendances)

def api_get_attendance():
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