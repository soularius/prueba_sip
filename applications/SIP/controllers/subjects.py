from applications.SIP.controllers.subjects_controller import SubjectsController

def list():
    controller = SubjectsController(db, SQLFORM)
    return controller.grid()


def create():
    controller = SubjectsController(db, SQLFORM)
    return controller.create()

def read():
    subject_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SubjectsController(db, SQLFORM)
    return controller.read(subject_id)

def update():
    subject_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SubjectsController(db, SQLFORM)
    return controller.update(subject_id)

def delete():
    subject_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SubjectsController(db, SQLFORM)
    controller.delete(subject_id)
    return