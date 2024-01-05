from applications.SIP.modules.factory.students_factory import StudentFactory
class APIStudent:    
    def __init__(self, db):
        self.db = db
        self.factory = StudentFactory(self.db)
    
    def create_student(self, student_data):
        # Validación de los datos
        if not student_data.get('name') or not student_data.get('lastname') or not student_data.get('email') or not student_data.get('phone'):
            return {'status': 'error', 'message': 'Missing required fields', 'http_status': 400}

        try:
            student = self.factory.get_or_create_student(student_data)
            return {'status': 'success', 'student_id': student.id, 'http_status': 201}
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'http_status': 500}
        
    def list_student(self, page=1, items_per_page=10):
        students = self.factory.list_students(page, items_per_page)
        students_list = [student.as_dict() for student in students]
        return {'students': students_list, 'http_status': 200}

    def get_student(self, student_id):
        student = self.factory.get_student(student_id)
        if student:
            return {'student': student.as_dict(), 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Student not found', 'http_status': 404}

    def update_student(self, student_id, student_data):
        student = self.factory.update_student(student_id, student_data)
        if student:
            return {'status': 'success', 'message': 'Student updated successfully', 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Student not found', 'http_status': 404}

    def delete_student(self, student_id):
        self.factory.delete_student(student_id)
        return {'status': 'success', 'message': 'Student deleted successfully', 'http_status': 200}

    def get_total_students(self):
        try:
            total_students = self.db(self.db.students.id > 0).count()
            return {'status': 'success', 'total_students': total_students, 'http_status': 200}
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'http_status': 500}