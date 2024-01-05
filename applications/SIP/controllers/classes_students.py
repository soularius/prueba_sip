from applications.SIP.controllers.classes_students_controller import ClassesStudentsController

def index():
    """
    Get the index of the classes and students.

    :return: The index of the classes and students.
    """
    controller = ClassesStudentsController(db, SQLFORM)
    return controller.index()