from .singleton_meta import SingletonMeta

class SalonFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_salon(self, id, name, description):
        if id not in self.cache:
            salon = self.db.salons.insert(id=id, name=name, description=description)
            self.cache[id] = salon
        return self.cache[id]