from applications.SIP.controllers.schedules_controller import SchedulesController

def index():
    """
    This function returns the result of calling the index() method of the SchedulesController class.

    :return: The result of calling the index() method of the SchedulesController class.
    :rtype: unknown
    """
    controller = SchedulesController(db, SQLFORM)
    return controller.index()