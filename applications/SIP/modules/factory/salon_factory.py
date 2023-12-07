from .singleton_meta import SingletonMeta

class SalonFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_salon(self, uuid, name, description):
        if uuid not in self.cache:
            salon = db.salons.insert(uuid=uuid, name=name, description=description)
            self.cache[uuid] = salon
        return self.cache[uuid]