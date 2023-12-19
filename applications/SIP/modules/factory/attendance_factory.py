from .singleton_meta import SingletonMeta

class AttendanceFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_attendance(self, id, student_id, class_id, date_class, status):
        if id not in self.cache:
            attendance = self.db.attendance.insert(student_id=student_id, class_id=class_id, date_class=date_class, status=status)
            self.cache[id] = attendance
        return self.cache[id]