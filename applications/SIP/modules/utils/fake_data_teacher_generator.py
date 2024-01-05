from faker import Faker
from applications.SIP.modules.factory.teacher_factory import TeacherFactory

class FakeDataTeacherGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')
        self.teacher_factory = TeacherFactory(db)

    def generate_static_teacher(self):
        """
        Generate a static teacher.

        This function generates a static teacher if one with the email "jhon.doe@example.es" does not already exist in the database. The generated teacher has the following data:
        - id: 1
        - name: "Jhon"
        - lastname: "Doe"
        - phone: "123456789"
        - email: "jhon.doe@example.es"

        Parameters:
            self (ClassName): An instance of the ClassName.

        Returns:
            None

        """
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
        """
        Generates a specified number of teacher records.

        Args:
            num_records (int): The number of teacher records to generate.

        Returns:
            None
        """
        for _ in range(num_records):
            teacher_data = {
                'name': self.fake.first_name(),
                'lastname': self.fake.last_name(),
                'phone': self.fake.phone_number(),
                'email': self.fake.unique.email()
            }

            self.teacher_factory.get_or_create_teacher(teacher_data)

        self.db.commit()
