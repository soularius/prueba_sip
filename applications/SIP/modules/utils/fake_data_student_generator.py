from faker import Faker
from applications.SIP.modules.factory.students_factory import StudentFactory

class FakeDataStudentGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')
        self.student_factory = StudentFactory(db)

    def generate_static_student(self):
        # Generar un estudiante estático
        if not self.db(self.db.students.email == "marta.salcedo@example.es").select().first():
            student_data = {
                'id': 1,
                'name': "Marta",
                'lastname': "Salcedo",
                'phone': "123456789",
                'email': "marta.salcedo@example.es"
            }
            self.student_factory.get_or_create_student(student_data)

    def generate_students(self, num_records):

        for _ in range(num_records):
            student_data = {
                'name': self.fake.first_name(),
                'lastname': self.fake.last_name(),
                'phone': self.fake.phone_number(),
                'email': self.fake.unique.email()
            }
            self.student_factory.get_or_create_student(student_data)
        
        self.db.commit()
