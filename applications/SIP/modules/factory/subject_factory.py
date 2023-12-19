from .singleton_meta import SingletonMeta

class SubjectFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_subject(self, id, name, description):
        if id not in self.cache:
            subject = self.db.subjects.insert(id=id, name=name, description=description)
            self.cache[id] = subject
        return self.cache[id]