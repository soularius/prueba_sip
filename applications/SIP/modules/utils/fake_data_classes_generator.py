from faker import Faker
import random

class FakeDataClassesGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()

    def generate_classes(self, num_records):
        salon_ids = self.db(self.db.salons.id > 0).select(self.db.salons.id)
        subject_ids = self.db(self.db.subjects.id > 0).select(self.db.subjects.id)
        schedule_ids = self.db(self.db.schedules.id > 0).select(self.db.schedules.id)
        teacher_ids = self.db(self.db.teachers.id > 0).select(self.db.teachers.id)
        day_of_week_ids = self.db(self.db.day_of_week.id > 0).select(self.db.day_of_week.id)

        for _ in range(num_records):
            self.db.classes.insert(
                code=self.fake.unique.lexify(text='????-????'),
                salon_id=random.choice(salon_ids).id,
                subject_id=random.choice(subject_ids).id,
                schedule_id=random.choice(schedule_ids).id,
                teacher_id=random.choice(teacher_ids).id,
                day_of_week_id=random.choice(day_of_week_ids).id
            )
        self.db.commit()
