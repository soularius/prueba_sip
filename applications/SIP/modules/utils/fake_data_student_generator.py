from faker import Faker

class FakeDataStudentGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')

    def generate_students(self, num_records):
        for _ in range(num_records):
            self.db.students.insert(
                name=self.fake.first_name(),
                lastname=self.fake.last_name(),
                phone=self.fake.phone_number(),
                email=self.fake.unique.email()
            )
        self.db.commit()
