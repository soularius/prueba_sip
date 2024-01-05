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
        # Generar un estudiante estático
        attendance_data = {
            'id': 1,
            'classes_students_id': 1,
            'date_class': self.fake.date_between(start_date="-1y", end_date="today"),
            'status': 1,
            'note': "Lorem ipsum dolor sit amet, consectetur adip A63, sed diam nonumy"
        }
        self.attendance_factory.get_or_create_attendance(attendance_data)

    def generate_attendance(self, num_records):
        classes_students_ids = [cs.id for cs in self.classes_students_factory.list_classes_students()]

        if not classes_students_ids:
            return
        
        # Primero, generar datos estáticos
        self.generate_static_attendance()

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
