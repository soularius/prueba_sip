from .singleton_meta import SingletonMeta

class TeacherFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_teacher(self, teacher_data):
        email = teacher_data.get('email')

        for teacher in self.cache.values():
            if teacher.email == email:
                return teacher

        existing_teacher = self.db(self.db.teachers.email == email).select().first()
        if existing_teacher:
            self.cache[existing_teacher.id] = existing_teacher
            return existing_teacher

        teacher_id = self.db.teachers.insert(**teacher_data)
        self.db.commit()

        new_teacher = self.db.teachers(teacher_id)
        self.cache[new_teacher.id] = new_teacher
        return new_teacher

    def get_teacher(self, teacher_id):
        if teacher_id in self.cache:
            return self.cache[teacher_id]

        teacher = self.db.teachers(teacher_id)
        if teacher:
            self.cache[teacher_id] = teacher
            return teacher
        return None

    def update_teacher(self, teacher_id, teacher_data):
        teacher = self.db.teachers(teacher_id)
        if teacher:
            teacher.update_record(**teacher_data)
            self.db.commit()
            self.cache[teacher_id] = teacher
            return teacher
        return None

    def delete_teacher(self, teacher_id):
        if teacher_id in self.cache:
            del self.cache[teacher_id]

        self.db(self.db.teachers.id == teacher_id).delete()
        self.db.commit()

    def list_teachers(self):
        teachers = self.db(self.db.teachers).select()
        for teacher in teachers:
            self.cache[teacher.id] = teacher
        return teachers
