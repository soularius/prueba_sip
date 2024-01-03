from applications.SIP.controllers.fake_generate_controller import FakeGenerateController

def index():
    controller = FakeGenerateController(db).index()
    return controller