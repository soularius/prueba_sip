from .singleton_meta import SingletonMeta

class ClassesFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_class(self, uuid, salon_uuid, subject_uuid, schedule_uuid, teacher_uuid, day_of_week_uuid):
        if uuid not in self.cache:
            class_instance = db.classes.insert(uuid=uuid, salon_uuid=salon_uuid, subject_uuid=subject_uuid, schedule_uuid=schedule_uuid, teacher_uuid=teacher_uuid, day_of_week_uuid=day_of_week_uuid)
            self.cache[uuid] = class_instance
        return self.cache[uuid]