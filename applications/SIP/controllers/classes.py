from applications.SIP.controllers.classes_controller import ClassesController

def index():
    controller = ClassesController(db, SQLFORM)
    return controller.index()

def create():
    controller = ClassesController(db, SQLFORM)
    return controller.create()

def read():
    classe_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = ClassesController(db, SQLFORM)
    return controller.read(classe_id)

def update():
    classe_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = ClassesController(db, SQLFORM)
    return controller.update(classe_id)

def delete():
    classe_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = ClassesController(db, SQLFORM)
    controller.delete(classe_id)
    return