from applications.SIP.controllers.subjects_controller import SubjectsController

def index():
    """
    Index function that returns the index of the subject controller.

    :return: The index of the subject controller.
    """
    controller = SubjectsController(db, SQLFORM)
    return controller.index()