from .singleton_meta import SingletonMeta

class ClassesStudentsFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_classes_students(self, id, class_id, student_id):
        if id not in self.cache:
            classes_students = self.db.classes_students.insert(id=id, class_id=class_id, student_id=student_id)
            self.cache[id] = classes_students
        return self.cache[id]