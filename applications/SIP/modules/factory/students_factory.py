from .singleton_meta import SingletonMeta

class StudentFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_student(self, id, name, lastname, phone, email):
        if id not in self.cache:
            student = self.db.students.insert(id=id, name=name, lastname=lastname, phone=phone, email=email)
            self.cache[id] = student
        return self.cache[id]