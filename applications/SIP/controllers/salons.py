from applications.SIP.controllers.salons_controller import SalonsController

def list():
    controller = SalonsController(db, SQLFORM)
    return controller.grid()


def create():
    controller = SalonsController(db, SQLFORM)
    return controller.create()

def read():
    salon_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SalonsController(db, SQLFORM)
    return controller.read(salon_id)

def update():
    salon_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SalonsController(db, SQLFORM)
    return controller.update(salon_id)

def delete():
    salon_id = request.args(0, cast=int) or redirect(URL('default', 'error'))
    controller = SalonsController(db, SQLFORM)
    controller.delete(salon_id)
    return