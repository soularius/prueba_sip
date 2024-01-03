from faker import Faker

class FakeDataSubjectGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')

    def generate_subjects(self, num_records):
        for _ in range(num_records):
            self.db.subjects.insert(
                name=self.fake.word().capitalize(),
                description=self.fake.text(max_nb_chars=200)
            )
        self.db.commit()
