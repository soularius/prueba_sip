from faker import Faker
from applications.SIP.modules.factory.salon_factory import SalonFactory
import random
import string

class FakeDataSalonGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')
        self.salon_factory = SalonFactory(db)

    def generate_salons(self, num_records):
        for _ in range(num_records):
            salon_name = f"{random.choice(string.ascii_uppercase)}{random.randint(1, 99):02d}"
            salon_data = {
                'name': salon_name,
                'description': self.fake.text(max_nb_chars=200)
            }

            self.salon_factory.get_or_create_salon(salon_data)

        self.db.commit()
