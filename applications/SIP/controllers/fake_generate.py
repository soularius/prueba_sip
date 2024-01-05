from applications.SIP.controllers.fake_generate_controller import FakeGenerateController

def index():
    """
    A function that returns the index controller.

    Returns:
        controller: The index controller.
    """
    controller = FakeGenerateController(db).index()
    return controller