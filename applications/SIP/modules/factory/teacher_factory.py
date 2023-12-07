from .singleton_meta import SingletonMeta

class TeacherFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_teacher(self, uuid, name, lastname, phone, email):
        if uuid not in self.cache:
            teacher = db.teachers.insert(uuid=uuid, name=name, lastname=lastname, phone=phone, email=email)
            self.cache[uuid] = teacher
        return self.cache[uuid]