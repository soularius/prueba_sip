from applications.SIP.controllers.schedules_controller import SchedulesController

def index():
    controller = SchedulesController(db, SQLFORM)
    return controller.index()