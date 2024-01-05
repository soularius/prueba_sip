from .singleton_meta import SingletonMeta

class StudentFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_student(self, student_data):
        email = student_data.get('email')
        for student in self.cache.values():
            if student.email == email:
                return student
            
        existing_student = self.db(self.db.students.email == email).select().first()
        if existing_student:
            self.cache[existing_student.id] = existing_student
            return existing_student
        
        student_id = self.db.students.insert(**student_data)
        self.db.commit()

        new_student = self.db.students(student_id)
        self.cache[new_student.id] = new_student
        return new_student

    def update_student(self, student_id, student_data):
        student = self.db.students(student_id)
        if student:
            student.update_record(**student_data)
            self.db.commit()
            self.cache[student_id] = student
            return student
        return None

    def delete_student(self, student_id):
        if student_id in self.cache:
            del self.cache[student_id]

        self.db(self.db.students.id == student_id).delete()
        self.db.commit()

    def get_student(self, student_id):
        if student_id in self.cache:
            return self.cache[student_id]

        student = self.db.students(student_id)
        if student:
            self.cache[student_id] = student
            return student
        return None

    def list_students(self, page, items_per_page):
        start = (page - 1) * items_per_page
        end = page * items_per_page
        students = self.db(self.db.students).select(orderby=self.db.students.id, limitby=(start, end))
        for student in students:
            self.cache[student.id] = student
        return students