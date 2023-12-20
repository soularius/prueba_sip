from applications.SIP.controllers.attendances_controller import AttendancesController

def index():
    controller = AttendancesController(db, SQLFORM)
    return controller.index()

def create():
    controller = AttendancesController(db, SQLFORM)
    return controller.create()

def read():
    attendance_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = AttendancesController(db, SQLFORM)
    return controller.read(attendance_id)

def update():
    attendance_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = AttendancesController(db, SQLFORM)
    return controller.update(attendance_id)

def delete():
    attendance_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = AttendancesController(db, SQLFORM)
    controller.delete(attendance_id)
    return