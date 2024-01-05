from .singleton_meta import SingletonMeta

class AttendanceFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_attendance(self, attendance_data):
        attendance = self.db.attendance.insert(**attendance_data)
        self.db.commit()
        self.cache[attendance.id] = attendance
        return attendance

    def update_attendance(self, attendance_id, attendance_data):
        attendance = self.db.attendance(attendance_id)
        if attendance:
            attendance.update_record(**attendance_data)
            self.db.commit()
            self.cache[attendance_id] = attendance
            return attendance
        return None

    def delete_attendance(self, attendance_id):
        if attendance_id in self.cache:
            del self.cache[attendance_id]

        self.db(self.db.attendance.id == attendance_id).delete()
        self.db.commit()

    def get_attendance(self, attendance_id):
        if attendance_id in self.cache:
            cached_attendance = self.cache[attendance_id]
            if cached_attendance is not None:
                return cached_attendance

        attendance = self.db.attendance(attendance_id)
        if attendance:
            self.cache[attendance_id] = attendance
            return attendance
        return None

    def list_attendances(self, page, items_per_page):
        start = (page - 1) * items_per_page
        end = page * items_per_page
        attendances = self.db(self.db.attendance).select(orderby=self.db.attendance.id, limitby=(start, end))
        for attendance in attendances:
            self.cache[attendance.id] = attendance
        return attendances