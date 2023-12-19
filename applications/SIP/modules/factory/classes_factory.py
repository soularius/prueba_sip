from .singleton_meta import SingletonMeta

class ClassesFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_class(self, id, salon_id, subject_id, schedule_id, teacher_id, day_of_week_id):
        if id not in self.cache:
            class_instance = self.db.classes.insert(id=id, salon_id=salon_id, subject_id=subject_id, schedule_id=schedule_id, teacher_id=teacher_id, day_of_week_id=day_of_week_id)
            self.cache[id] = class_instance
        return self.cache[id]