from faker import Faker
from applications.SIP.modules.factory.subject_factory import SubjectFactory

class FakeDataSubjectGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')
        self.subject_factory = SubjectFactory(db)

    def generate_static_subject(self):
        subject_data = {
            'id': 1,
            'name': "Fisica",
            'description': "Lorem ipsum dolor sit amet, consectetur adip Fisica, sed do eiusmod tempor incididunt ut labore et"
        }
        self.subject_factory.get_or_create_subject(subject_data)

    def generate_subjects(self, num_records):
        # Primero, generar datos estáticos
        self.generate_static_subject()

        for _ in range(num_records):
            subject_data = {
                'name': self.fake.word().capitalize(),
                'description': self.fake.text(max_nb_chars=200)
            }

            self.subject_factory.get_or_create_subject(subject_data)


        self.db.commit()