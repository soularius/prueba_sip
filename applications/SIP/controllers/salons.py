from applications.SIP.controllers.salons_controller import SalonsController

def index():
    controller = SalonsController(db, SQLFORM)
    return controller.index()