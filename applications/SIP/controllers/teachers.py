from applications.SIP.controllers.teachers_controller import TeachersController

def index():
    controller = TeachersController(db, SQLFORM)
    return controller.index()