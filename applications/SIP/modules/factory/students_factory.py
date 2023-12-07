from .singleton_meta import SingletonMeta

class StudentFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_student(self, uuid, name, lastname, phone, email):
        if uuid not in self.cache:
            student = db.students.insert(uuid=uuid, name=name, lastname=lastname, phone=phone, email=email)
            self.cache[uuid] = student
        return self.cache[uuid]