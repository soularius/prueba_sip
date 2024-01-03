from applications.SIP.controllers.classes_controller import ClassesController

def index():
    controller = ClassesController(db, SQLFORM)
    return controller.index()