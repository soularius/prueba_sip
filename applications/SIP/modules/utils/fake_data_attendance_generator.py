from faker import Faker
import random
from datetime import timedelta

class FakeDataAttendanceGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()

    def generate_attendance(self, num_records):
        classes_students_ids = self.db(self.db.classes_students.id > 0).select(self.db.classes_students.id)

        for _ in range(num_records):
            date_class = self.fake.date_between(start_date="-1y", end_date="today")
            status = random.randint(0, 1)  # 0 para ausente, 1 para presente

            self.db.attendance.insert(
                classes_students_id=random.choice(classes_students_ids).id,
                date_class=date_class,
                status=status,
                note=self.fake.text(max_nb_chars=200)
            )
        self.db.commit()
