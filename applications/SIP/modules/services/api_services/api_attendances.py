from applications.SIP.modules.factory.attendance_factory import AttendanceFactory

class APIAttendance:
    def __init__(self, db):
        self.db = db
        self.factory = AttendanceFactory(db)
    
    def create_attendance(self, attendance_data):
        try:
            attendance = self.factory.get_or_create_attendance(attendance_data)
            return {'status': 'success', 'attendance_id': attendance.id, 'http_status': 201}
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'http_status': 500}

    def list_attendance(self, page=1, items_per_page=10):
        attendances = self.factory.list_attendances(page, items_per_page)
        attendances_list = [attendance.as_dict() for attendance in attendances]
        return {'attendances': attendances_list, 'http_status': 200}

    def get_attendance(self, attendance_id):
        attendance = self.factory.get_attendance(attendance_id)
        if attendance is not None:
            return {'attendance': attendance, 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Attendance not found', 'http_status': 404}

    def update_attendance(self, attendance_id, attendance_data):
        attendance = self.factory.update_attendance(attendance_id, attendance_data)
        if attendance:
            return {'status': 'success', 'message': 'Attendance updated successfully', 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Attendance not found', 'http_status': 404}

    def delete_attendance(self, attendance_id):
        self.factory.delete_attendance(attendance_id)
        return {'status': 'success', 'message': 'Attendance deleted successfully', 'http_status': 200}