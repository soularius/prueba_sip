from .singleton_meta import SingletonMeta

class AttendanceFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        """
        Initializes a new instance of the class.
        
        Args:
            db: The database object to be used.
        
        Returns:
            None
        """
        self.db = db
        self.cache = {}

    def get_or_create_attendance(self, attendance_data):
        """
        Get or create attendance record.

        Args:
            attendance_data (dict): A dictionary containing the attendance data.

        Returns:
            Attendance: The attendance record that was created or retrieved.

        """
        attendance = self.db.attendance.insert(**attendance_data)
        self.db.commit()
        self.cache[attendance.id] = attendance
        return attendance

    def update_attendance(self, attendance_id, attendance_data):
        """
        Update the attendance record with the given attendance ID.

        :param attendance_id: The ID of the attendance record to update.
        :type attendance_id: int

        :param attendance_data: The new data to update the attendance record with.
        :type attendance_data: dict

        :return: The updated attendance record, or None if the attendance record does not exist.
        :rtype: dict or None
        """
        attendance = self.db.attendance(attendance_id)
        if attendance:
            attendance.update_record(**attendance_data)
            self.db.commit()
            self.cache[attendance_id] = attendance
            return attendance
        return None

    def delete_attendance(self, attendance_id):
        """
        Deletes an attendance record from the cache and the database.

        Parameters:
            attendance_id (int): The ID of the attendance record to be deleted.

        Returns:
            None
        """
        if attendance_id in self.cache:
            del self.cache[attendance_id]

        self.db(self.db.attendance.id == attendance_id).delete()
        self.db.commit()

    def get_attendance(self, attendance_id):
        """
        Retrieves the attendance record for a given attendance ID.

        Parameters:
            attendance_id (int): The ID of the attendance record to retrieve.

        Returns:
            attendance (dict): The attendance record if found, None otherwise.
        """
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
        """
        Retrieves a list of attendances based on the specified page and items per page.

        :param page: The page number to retrieve.
        :type page: int
        :param items_per_page: The number of items per page.
        :type items_per_page: int
        :return: A list of attendances.
        :rtype: List[Attendance]
        """
        start = (page - 1) * items_per_page
        end = page * items_per_page
        attendances = self.db(self.db.attendance).select(orderby=self.db.attendance.id, limitby=(start, end))
        for attendance in attendances:
            self.cache[attendance.id] = attendance
        return attendances