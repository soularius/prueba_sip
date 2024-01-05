from faker import Faker
from applications.SIP.modules.factory.subject_factory import SubjectFactory

class FakeDataSubjectGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')
        self.subject_factory = SubjectFactory(db)

    def generate_static_subject(self):
        """
        Generate a static subject if it does not exist in the database.

        This method checks if the subject with the name "Fisica" exists in the database. If it does not exist, it creates a new subject with the following data:
        - id: 1
        - name: "Fisica"
        - description: "Lorem ipsum dolor sit amet, consectetur adip Fisica, sed do eiusmod tempor incididunt ut labore et"

        Parameters:
        - None

        Returns:
        - None
        """
        if not self.db(self.db.subjects.name == "Fisica").select().first():
            subject_data = {
                'id': 1,
                'name': "Fisica",
                'description': "Lorem ipsum dolor sit amet, consectetur adip Fisica, sed do eiusmod tempor incididunt ut labore et"
            }
            self.subject_factory.get_or_create_subject(subject_data)

    def generate_subjects(self, num_records):
        """
        Generate subjects and save them to the database.

        Args:
            num_records (int): The number of subjects to generate.

        Returns:
            None
        """

        for _ in range(num_records):
            subject_data = {
                'name': self.fake.word().capitalize(),
                'description': self.fake.text(max_nb_chars=200)
            }

            self.subject_factory.get_or_create_subject(subject_data)


        self.db.commit()