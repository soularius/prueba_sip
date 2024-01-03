from faker import Faker
import random

class FakeDataScheduleGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()

    def generate_schedules(self, num_records):
        for _ in range(num_records):
            # Genera una hora de inicio aleatoria entre las 7:00 y las 15:00
            hour_start = random.randint(7, 15)
            minute_start = random.choice([0, 30])  # Horas en punto o y media
            time_start = f"{hour_start:02d}:{minute_start:02d}"

            # La hora de fin es una o dos horas después de la hora de inicio
            hour_end = hour_start + random.choice([1, 2])
            time_end = f"{hour_end:02d}:{minute_start:02d}"

            self.db.schedules.insert(
                block_start=time_start,
                block_end=time_end
            )
        self.db.commit()
