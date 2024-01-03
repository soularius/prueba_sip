from applications.SIP.controllers.subjects_controller import SubjectsController

def index():
    controller = SubjectsController(db, SQLFORM)
    return controller.index()