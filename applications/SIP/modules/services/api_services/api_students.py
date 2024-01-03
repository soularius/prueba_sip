
class APIStudent:    
    def __init__(self, db):
        self.db = db
    
    def create_student(self, student_data):
        # Validación de los datos
        if not student_data.get('name') or not student_data.get('lastname') or not student_data.get('email') or not student_data.get('phone'):
            return {'status': 'error', 'message': 'Missing required fields'}

        try:
            student_id = self.db.students.insert(**student_data)
            self.db.commit()
            return {'status': 'success', 'student_id': student_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def list_student(self, page=1, items_per_page=10):
        start = (page - 1) * items_per_page
        end = page * items_per_page
        students = self.db(self.db.students).select(orderby=self.db.students.id, limitby=(start, end))
        if students:
            # Convertir cada registro de estudiante a un diccionario y agregarlos a una lista
            students_list = [student.as_dict() for student in students]
            return students_list
        else:
            return {'status': 'error', 'message': 'No students found'}

    def get_student(self, student_id):
        student = self.db.students(student_id)
        if student:
            return student.as_dict()
        else:
            return {'status': 'error', 'message': 'Student not found'}

    def update_student(self, student_id, student_data):
        student = self.db.students(student_id)
        if student:
            student.update_record(**student_data)
            self.db.commit()
            return {'status': 'success', 'message': 'Student updated successfully'}
        else:
            return {'status': 'error', 'message': 'Student not found'}

    def delete_student(self, student_id):
        student = self.db.students(student_id)
        if student:
            self.db(self.db.students.id == student_id).delete()
            self.db.commit()
            return {'status': 'success', 'message': 'Student deleted successfully'}
        else:
            return {'status': 'error', 'message': 'Student not found'}