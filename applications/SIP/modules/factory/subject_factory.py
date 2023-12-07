from .singleton_meta import SingletonMeta

class SubjectFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_subject(self, uuid, name, description):
        if uuid not in self.cache:
            subject = self.db.subjects.insert(uuid=uuid, name=name, description=description)
            self.cache[uuid] = subject
        return self.cache[uuid]