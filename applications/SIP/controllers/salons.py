from applications.SIP.controllers.salons_controller import SalonsController

def index():
    """
        A function that returns the index of a salon.

        Params:
            None
            
        Returns:
            The index of the salon.
    """
    controller = SalonsController(db, SQLFORM)
    return controller.index()