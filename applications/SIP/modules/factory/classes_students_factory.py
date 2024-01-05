from .singleton_meta import SingletonMeta

class ClassesStudentsFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_classes_student(self, classes_student_data):
        section_class_student = classes_student_data.get('section_class')
        for class_student_obj in self.cache.values():
            if class_student_obj.section_class == section_class_student:
                return class_student_obj
            
        existing_class_student = self.db(self.db.classes_students.section_class == section_class_student).select().first()
        if existing_class_student:
            self.cache[existing_class_student.id] = existing_class_student
            return existing_class_student
        
        class_id = self.db.classes_students.insert(**classes_student_data)
        self.db.commit()

        new_class_student = self.db.classes_students(class_id)
        self.cache[new_class_student.id] = new_class_student
        return new_class_student

    def get_classes_student(self, classes_student_id):
        if classes_student_id in self.cache:
            return self.cache[classes_student_id]

        classes_student = self.db.classes_students(classes_student_id)
        if classes_student:
            self.cache[classes_student_id] = classes_student
            return classes_student
        return None

    def update_classes_student(self, classes_student_id, classes_student_data):
        classes_student = self.db.classes_students(classes_student_id)
        if classes_student:
            classes_student.update_record(**classes_student_data)
            self.db.commit()
            self.cache[classes_student_id] = classes_student
            return classes_student
        return None

    def delete_classes_student(self, classes_student_id):
        if classes_student_id in self.cache:
            del self.cache[classes_student_id]

        self.db(self.db.classes_students.id == classes_student_id).delete()
        self.db.commit()

    def list_classes_students(self):
        classes_students = self.db(self.db.classes_students).select()
        for classes_student in classes_students:
            self.cache[classes_student.id] = classes_student
        return classes_students