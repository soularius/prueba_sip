from applications.SIP.controllers.teachers_controller import TeachersController

def index():
    controller = TeachersController(db, SQLFORM)
    return controller.index()


def create():
    controller = TeachersController(db, SQLFORM)
    return controller.create()

def read():
    teacher_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = TeachersController(db, SQLFORM)
    return controller.read(teacher_id)

def update():
    teacher_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = TeachersController(db, SQLFORM)
    return controller.update(teacher_id)

def delete():
    teacher_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = TeachersController(db, SQLFORM)
    controller.delete(teacher_id)
    return