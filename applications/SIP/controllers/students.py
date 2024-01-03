from applications.SIP.controllers.students_controller import StudentsController

def index():
    controller = StudentsController(db, SQLFORM)
    return controller.index()