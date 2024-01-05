from faker import Faker
from applications.SIP.modules.factory.schedule_factory import ScheduleFactory
import random

class FakeDataScheduleGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()
        self.schedule_factory = ScheduleFactory(db)

    def generate_schedules(self, num_records):
        """
        Generates schedules based on the given number of records.
        
        Args:
            num_records (int): The number of schedules to generate.
        
        Returns:
            None
        
        Raises:
            None
        """
        for _ in range(num_records):
            hour_start = random.randint(7, 15)
            minute_start = random.choice([0, 30])
            time_start = f"{hour_start:02d}:{minute_start:02d}"

            hour_end = hour_start + random.choice([1, 2])
            time_end = f"{hour_end:02d}:{minute_start:02d}"

            schedule_data = {
                'block_start': time_start,
                'block_end': time_end
            }

            self.schedule_factory.get_or_create_schedule(schedule_data)

        self.db.commit()
