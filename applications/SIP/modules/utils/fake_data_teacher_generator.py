from faker import Faker
from applications.SIP.modules.factory.teacher_factory import TeacherFactory

class FakeDataTeacherGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')
        self.teacher_factory = TeacherFactory(db)

    def generate_static_teacher(self):
        # Generar un estudiante estático
        if not self.db(self.db.teachers.email == "jhon.doe@example.es").select().first():
            teacher_data = {
                'id': 1,
                'name': "Jhon",
                'lastname': "Doe",
                'phone': "123456789",
                'email': "jhon.doe@example.es"
            }
            self.teacher_factory.get_or_create_teacher(teacher_data)

    def generate_teachers(self, num_records):
        for _ in range(num_records):
            teacher_data = {
                'name': self.fake.first_name(),
                'lastname': self.fake.last_name(),
                'phone': self.fake.phone_number(),
                'email': self.fake.unique.email()
            }

            self.teacher_factory.get_or_create_teacher(teacher_data)

        self.db.commit()
