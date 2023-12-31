from faker import Faker
import random
from datetime import timedelta
from applications.SIP.modules.factory.attendance_factory import AttendanceFactory
from applications.SIP.modules.factory.classes_students_factory import ClassesStudentsFactory

class FakeDataAttendanceGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()
        self.attendance_factory = AttendanceFactory(db)
        self.classes_students_factory = ClassesStudentsFactory(db)

    def generate_static_attendance(self):
        """
        Generate a static attendance.

        This function generates a static attendance for a student. If there is no attendance record with the note "A63A01A45T" in the database, a new attendance record is created.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        # Generar un estudiante estático
        if not self.db(self.db.attendance.note == "A63A01A45T").select().first():
            attendance_data = {
                'id': 1,
                'classes_students_id': 1,
                'date_class': self.fake.date_between(start_date="-1y", end_date="today"),
                'status': 1,
                'note': "A63A01A45T"
            }
            self.attendance_factory.get_or_create_attendance(attendance_data)

    def generate_attendance(self, num_records):
        """
        Generates attendance records for a specified number of records.

        Parameters:
            num_records (int): The number of attendance records to generate.

        Returns:
            None
        """
        classes_students_ids = [cs.id for cs in self.classes_students_factory.list_classes_students()]

        if not classes_students_ids:
            return

        for _ in range(num_records):
            date_class = self.fake.date_between(start_date="-1y", end_date="today")
            status = random.randint(0, 1)  # 0 para ausente, 1 para presente

            attendance_data = {
                'classes_students_id': random.choice(classes_students_ids),
                'date_class': date_class,
                'status': status,
                'note': self.fake.text(max_nb_chars=200)
            }
            self.attendance_factory.get_or_create_attendance(attendance_data)
        self.db.commit()
