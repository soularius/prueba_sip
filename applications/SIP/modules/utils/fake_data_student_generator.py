from faker import Faker
from applications.SIP.modules.factory.students_factory import StudentFactory

class FakeDataStudentGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')
        self.student_factory = StudentFactory(db)

    def generate_static_student(self):
        """
        Generates a static student.

        This function checks if a student with the email "marta.salcedo@example.es" already exists in the database. If not, it creates a new student with the following data:
        - id: 1
        - name: "Marta"
        - lastname: "Salcedo"
        - phone: "123456789"
        - email: "marta.salcedo@example.es"

        This function does not have any parameters.
        This function does not have a return value.
        """
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
        """
        Generates a specified number of student records.

        Parameters:
            num_records (int): The number of student records to generate.

        Returns:
            None

        """

        for _ in range(num_records):
            student_data = {
                'name': self.fake.first_name(),
                'lastname': self.fake.last_name(),
                'phone': self.fake.phone_number(),
                'email': self.fake.unique.email()
            }
            self.student_factory.get_or_create_student(student_data)
        
        self.db.commit()
