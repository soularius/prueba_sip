from faker import Faker
import random
import string

class FakeDataSalonGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')

    def generate_salons(self, num_records):
        for _ in range(num_records):
            salon_name = f"{random.choice(string.ascii_uppercase)}{random.randint(1, 99):02d}"
            self.db.salons.insert(
                name=salon_name,
                description=self.fake.text(max_nb_chars=200)
            )
        self.db.commit()
