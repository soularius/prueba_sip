from applications.SIP.controllers.day_of_weeks_controller import DayOfWeeksController

def index():
    controller = DayOfWeeksController(db, SQLFORM)
    return controller.index()

def create():
    controller = DayOfWeeksController(db, SQLFORM)
    return controller.create()

def read():
    classe_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = DayOfWeeksController(db, SQLFORM)
    return controller.read(classe_id)

def update():
    classe_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = DayOfWeeksController(db, SQLFORM)
    return controller.update(classe_id)

def delete():
    classe_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = DayOfWeeksController(db, SQLFORM)
    controller.delete(classe_id)
    return