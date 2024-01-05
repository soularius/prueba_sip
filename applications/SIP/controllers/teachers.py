from applications.SIP.controllers.teachers_controller import TeachersController

def index():
    """
    A function that returns the result of calling the `index()` method of the `TeachersController` class.
    """
    controller = TeachersController(db, SQLFORM)
    return controller.index()