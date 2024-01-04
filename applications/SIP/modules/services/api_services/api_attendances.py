class APIAttendance:
    def __init__(self, db):
        self.db = db

    def create_attendance(self, attendance_data):
        try:
            attendance_id = self.db.attendance.insert(**attendance_data)
            self.db.commit()
            return {'status': 'success', 'attendance_id': attendance_id, 'http_status': 201}
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'http_status': 500}

    def get_attendance(self, attendance_id):
        attendance = self.db.attendance(attendance_id)
        if attendance:
            return {'attendance': attendance.as_dict(), 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Attendance not found', 'http_status': 404}

    def list_attendance(self, page=1, items_per_page=10):
        start = (page - 1) * items_per_page
        end = page * items_per_page
        attendances = self.db(self.db.attendance).select(orderby=self.db.attendance.id, limitby=(start, end))
        if attendances:
            # Convertir cada registro de estudiante a un diccionario y agregarlos a una lista
            attendances_list = [attendance.as_dict() for attendance in attendances]
            return {'attendances': attendances_list, 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'No students found', 'http_status': 404}
        
    def update_attendance(self, attendance_id, attendance_data):
        attendance = self.db.attendance(attendance_id)
        if attendance:
            attendance.update_record(**attendance_data)
            self.db.commit()
            return {'status': 'success', 'message': 'Attendance updated successfully', 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Attendance not found', 'http_status': 404}

    def delete_attendance(self, attendance_id):
        attendance = self.db.attendance(attendance_id)
        if attendance:
            self.db(self.db.attendance.id == attendance_id).delete()
            self.db.commit()
            return {'status': 'success', 'message': 'Attendance deleted successfully', 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Attendance not found', 'http_status': 404}
