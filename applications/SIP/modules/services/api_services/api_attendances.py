from applications.SIP.modules.factory.attendance_factory import AttendanceFactory

class APIAttendance:
    """
    API class for managing attendance records.

    Provides an interface for creating, listing, retrieving, updating, and deleting
    attendance records. Utilizes the AttendanceFactory class for database operations.

    Attributes:
        db: An instance of the database.
        factory: An instance of AttendanceFactory for handling attendance-related operations.

    Methods:
        create_attendance(attendance_data): Creates a new attendance record.
        list_attendance(page, items_per_page): Lists attendance records with pagination.
        get_attendance(attendance_id): Retrieves a specific attendance record by ID.
        update_attendance(attendance_id, attendance_data): Updates an existing attendance record.
        delete_attendance(attendance_id): Deletes an attendance record by ID.
    """
    def __init__(self, db):
        """
        Initializes the APIAttendance class with a database instance and an instance of AttendanceFactory.

        Args:
            db: An instance of the database.
        """
        self.db = db
        self.factory = AttendanceFactory(db)
    
    def create_attendance(self, attendance_data):
        """
        Creates a new attendance record in the database.

        Args:
            attendance_data: A dictionary containing data for the new attendance record.

        Returns:
            A dictionary with the status of the operation, attendance ID if created, and the HTTP status code.
        """
        try:
            attendance = self.factory.get_or_create_attendance(attendance_data)
            return {'status': 'success', 'attendance_id': attendance.id, 'http_status': 201}
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'http_status': 500}

    def list_attendance(self, page=1, items_per_page=10):
        """
        Lists attendance records with pagination.

        Args:
            page: The page number for pagination (default is 1).
            items_per_page: The number of items per page (default is 10).

        Returns:
            A dictionary containing a list of attendance records and the HTTP status code.
        """
        attendances = self.factory.list_attendances(page, items_per_page)
        attendances_list = [attendance.as_dict() for attendance in attendances]
        return {'attendances': attendances_list, 'http_status': 200}

    def get_attendance(self, attendance_id):
        """
        Retrieves a specific attendance record by its ID.

        Args:
            attendance_id: The ID of the attendance record to be retrieved.

        Returns:
            A dictionary containing the attendance record if found, along with the HTTP status code.
            If not found, returns a dictionary with an error message and the HTTP status code.
        """
        attendance = self.factory.get_attendance(attendance_id)
        if attendance is not None:
            return {'attendance': attendance, 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Attendance not found', 'http_status': 404}

    def update_attendance(self, attendance_id, attendance_data):
        """
        Updates an existing attendance record identified by its ID.

        Args:
            attendance_id: The ID of the attendance record to be updated.
            attendance_data: A dictionary containing the updated data for the attendance record.

        Returns:
            A dictionary with the status of the operation, a message, and the HTTP status code.
        """
        attendance = self.factory.update_attendance(attendance_id, attendance_data)
        if attendance:
            return {'status': 'success', 'message': 'Attendance updated successfully', 'http_status': 200}
        else:
            return {'status': 'error', 'message': 'Attendance not found', 'http_status': 404}

    def delete_attendance(self, attendance_id):
        """
        Deletes an attendance record identified by its ID.

        Args:
            attendance_id: The ID of the attendance record to be deleted.

        Returns:
            A dictionary with the status of the operation, a message, and the HTTP status code.
        """
        self.factory.delete_attendance(attendance_id)
        return {'status': 'success', 'message': 'Attendance deleted successfully', 'http_status': 200}