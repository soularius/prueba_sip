from applications.SIP.controllers.classes_students_controller import ClassesStudentsController

def index():
    controller = ClassesStudentsController(db, SQLFORM)
    return controller.index()