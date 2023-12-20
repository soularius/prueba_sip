from applications.SIP.controllers.schedules_controller import SchedulesController

def index():
    controller = SchedulesController(db, SQLFORM)
    return controller.index()

def create():
    controller = SchedulesController(db, SQLFORM)
    return controller.create()

def read():
    salon_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SchedulesController(db, SQLFORM)
    return controller.read(salon_id)

def update():
    salon_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SchedulesController(db, SQLFORM)
    return controller.update(salon_id)

def delete():
    salon_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SchedulesController(db, SQLFORM)
    controller.delete(salon_id)
    return