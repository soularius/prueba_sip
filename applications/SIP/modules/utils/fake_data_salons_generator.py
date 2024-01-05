from faker import Faker
from applications.SIP.modules.factory.salon_factory import SalonFactory
import random
import string

class FakeDataSalonGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker('es_CO')
        self.salon_factory = SalonFactory(db)

    def generate_static_salon(self):
        if not self.db(self.db.salons.name == "A63").select().first():
            salon_data = {
                'id': 1,
                'name': "A63",
                'description': "Lorem ipsum dolor sit amet, consectetur adip A63, sed diam nonumy"
            }
            self.salon_factory.get_or_create_salon(salon_data)

    def generate_salons(self, num_records):

        for _ in range(num_records):
            salon_name = f"{random.choice(string.ascii_uppercase)}{random.randint(1, 99):02d}"
            salon_data = {
                'name': salon_name,
                'description': self.fake.text(max_nb_chars=200)
            }

            self.salon_factory.get_or_create_salon(salon_data)

        self.db.commit()
