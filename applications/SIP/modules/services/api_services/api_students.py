from applications.SIP.modules.factory.students_factory import StudentFactory
class APIStudent:
    """
    API class for managing student records.

    Provides an interface for creating, listing, retrieving, updating, and deleting
    student records. Utilizes the StudentFactory class for database operations.

    Attributes:
        db: An instance of the database.
        factory: An instance of StudentFactory for handling student-related operations.

    Methods:
        create_student(student_data): Creates a new student record.
        list_student(page, items_per_page): Lists student records with pagination.
        get_student(student_id): Retrieves a specific student record by ID.
        update_student(student_id, student_data): Updates an existing student record.
        delete_student(student_id): Deletes a student record by ID.
        get_total_students(): Retrieves the total number of students.
    """
    def __init__(self, db):
        """
        Initializes the APIStudent class with a database instance and an instance of StudentFactory.

        Args:
            db: An instance of the database.
        """
        self.db = db
        self.factory = StudentFactory(self.db)
    
    def create_student(self, student_data):
        """
        Creates a new student record in the database.

        Args:
            student_data: A dictionary containing data for the new student record.

        Returns:
            A dictionary with the status of the operation, student ID if created, and the HTTP status code.
        """
        # Data validation
        if not student_data.get('name') or not student_data.get('lastname') or not student_data.get('email') or not student_data.get('phone'):
            return {'status': 'error', 'message': 'Missing required fields', 'http_status': 400}

        try:
            student = self.factory.get_or_create_student(student_data)
            return {'status': 'success', 'student_id': student.id, 'http_status': 201}
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'http_status': 500}
        
    def list_student(self, page=1, items_per_page=10):
        """
        Lists student records with pagination.

        Args:
            page: The page number for pagination (default is 1).
            items_per_page: The number of items per page (default is 10).

        Returns:
            A dictionary containing a list of student records and the HTTP status code.
        """
        students = self.factory.list_students(page, items_per_page)
        students_list = [student.as_dict() for student in students]
        return {'students': students_list, 'http_status': 200}

    def get_student(self, student_id):
        """
        Retrieves a specific student record by its ID.

        Args:
            student_id: The ID of the student record to be retrieved.

        Returns:
            A dictionary containing the student record if found, along with the HTTP status code.
            If not found, returns a dictionary with an error message and the HTTP status code.
        """
        student = self.factory.get_student(student_id)
        if student:
            return {'student': student.as_dict(), 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Student not found', 'http_status': 404}

    def update_student(self, student_id, student_data):
        """
        Updates an existing student record identified by its ID.

        Args:
            student_id: The ID of the student record to be updated.
            student_data: A dictionary containing the updated data for the student record.

        Returns:
            A dictionary with the status of the operation, a message, and the HTTP status code.
        """
        student = self.factory.update_student(student_id, student_data)
        if student:
            return {'status': 'success', 'message': 'Student updated successfully', 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Student not found', 'http_status': 404}

    def delete_student(self, student_id):
        """
        Deletes a student record identified by its ID.

        Args:
            student_id: The ID of the student record to be deleted.

        Returns:
            A dictionary with the status of the operation, a message, and the HTTP status code.
        """
        self.factory.delete_student(student_id)
        return {'status': 'success', 'message': 'Student deleted successfully', 'http_status': 200}

    def get_total_students(self):
        """
        Retrieves the total number of student records in the database.

        Returns:
            A dictionary with the status of the operation, total number of students, and the HTTP status code.
        """
        try:
            total_students = self.db(self.db.students.id > 0).count()
            return {'status': 'success', 'total_students': total_students, 'http_status': 200}
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'http_status': 500}