from applications.SIP.controllers.day_of_weeks_controller import DayOfWeeksController

def index():
    controller = DayOfWeeksController(db, SQLFORM)
    return controller.index()