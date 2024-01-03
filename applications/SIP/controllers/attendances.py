from applications.SIP.controllers.attendances_controller import AttendancesController

def index():
    controller = AttendancesController(db, SQLFORM)
    return controller.index()