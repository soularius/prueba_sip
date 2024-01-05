from applications.SIP.controllers.day_of_weeks_controller import DayOfWeeksController

def index():
    """
    A function that returns the index of the DayOfWeeksController.

    Returns:
        The index of the DayOfWeeksController.
    """
    controller = DayOfWeeksController(db, SQLFORM)
    return controller.index()