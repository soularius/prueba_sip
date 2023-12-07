from .singleton_meta import SingletonMeta

class ClassesStudentsFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_classes_students(self, uuid, class_uuid, student_uuid):
        if uuid not in self.cache:
            classes_students = self.db.classes_students.insert(uuid=uuid, class_uuid=class_uuid, student_uuid=student_uuid)
            self.cache[uuid] = classes_students
        return self.cache[uuid]