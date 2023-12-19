from .singleton_meta import SingletonMeta

class TeacherFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_teacher(self, id, name, lastname, phone, email):
        if id not in self.cache:
            teacher = self.db.teachers.insert(name=name, lastname=lastname, phone=phone, email=email)
            self.cache[id] = teacher
        return self.cache[id]