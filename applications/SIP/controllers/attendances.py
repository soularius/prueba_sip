from applications.SIP.controllers.attendances_controller import AttendancesController
from applications.SIP.modules.renderer.renderer_attendance import RendererAttendance
from applications.SIP.modules.services.api_services.api_attendances import APIAttendance

def index():
    controller = AttendancesController(db, SQLFORM)
    return controller.index()

def attendance_view():
    page = request.args(0, cast=int, default=0)
    items_per_page = 10
    total_records = db(db.attendance).count()
    total_pages = (total_records // items_per_page) + (1 if total_records % items_per_page else 0)

    if page >= total_pages:
        redirect(URL('attendance_view', args=[total_pages-1 if total_pages > 0 else 0]))

    limitby = (page*items_per_page, (page+1)*items_per_page)

    attendance_records = db(db.attendance).select(
        orderby=db.attendance.id, 
        limitby=limitby
    )

    renderer = RendererAttendance(db)
    attendance_table = renderer.render_view(attendance_records)

    return dict(table=attendance_table, items_per_page=items_per_page, page=page)

def attendance_update():
    record_id = request.args(0, cast=int, default=0)
    new_status_key = f'status_{record_id}'
    new_status = request.vars.get(new_status_key)

    if record_id and new_status is not None:
        db(db.attendance.id == record_id).update(status=new_status)
        response.flash = "Estatus actualizado."
    else:
        response.flash = "Error al actualizar."
    return dict()

def api_list_attendance():
    page = int(request.vars.page or 1)
    page_size = int(request.vars.page_size or 10)
    api_attendance = APIAttendance(db)
    attendances = api_attendance.list_attendance(page, page_size)
    return response.json(attendances)

def api_get_attendance():
    attendance_id = request.args(0)  # Obtener el ID del estudiante de los argumentos URL
    if attendance_id:
        api_attendance = APIAttendance(db)
        result = api_attendance.get_attendance(attendance_id)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'No student ID provided'})

def api_create_attendance():
    if request.env.request_method == 'POST':
        api_attendance = APIAttendance(db)
        result = api_attendance.create_attendance(request.post_vars)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request method'})

def api_update_attendance():
    attendance_id = request.args(0)  # Obtener el ID del estudiante de los argumentos URL
    if attendance_id and request.env.request_method in ['PUT', 'POST']:
        api_attendance = APIAttendance(db)
        attendance_data = request.post_vars
        result = api_attendance.update_attendance(attendance_id, attendance_data)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request'})

def api_delete_attendance():
    attendance_id = request.args(0)  # Obtener el ID del estudiante de los argumentos URL
    if attendance_id and request.env.request_method == 'DELETE':
        api_attendance = APIAttendance(db)
        result = api_attendance.delete_attendance(attendance_id)
        return response.json(result)
    else:
        return response.json({'status': 'error', 'error_message': 'Invalid request'})