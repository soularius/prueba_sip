from .singleton_meta import SingletonMeta

class AttendanceFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_attendance(self, uuid, student_uuid, class_uuid, date_class, status):
        if uuid not in self.cache:
            attendance = db.attendance.insert(uuid=uuid, student_uuid=student_uuid, class_uuid=class_uuid, date_class=date_class, status=status)
            self.cache[uuid] = attendance
        return self.cache[uuid]