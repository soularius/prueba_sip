from faker import Faker
import random
from applications.SIP.modules.factory.classes_factory import ClassesFactory
from applications.SIP.modules.factory.salon_factory import SalonFactory
from applications.SIP.modules.factory.subject_factory import SubjectFactory
from applications.SIP.modules.factory.schedule_factory import ScheduleFactory
from applications.SIP.modules.factory.teacher_factory import TeacherFactory
from applications.SIP.modules.factory.day_of_week_factory import DayOfWeekFactory

class FakeDataClassesGenerator:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()
        self.classes_factory = ClassesFactory(db)
        self.salon_factory = SalonFactory(db)
        self.subject_factory = SubjectFactory(db)
        self.schedule_factory = ScheduleFactory(db)
        self.teacher_factory = TeacherFactory(db)
        self.day_of_week_factory = DayOfWeekFactory(db)

    def generate_static_class(self):
        schedule_ids = [schedule.id for schedule in self.schedule_factory.list_schedules()]
        day_of_week_ids = [day.id for day in self.day_of_week_factory.list_days_of_week()]
        class_data = {
            'id': 1,
            'code': "A01",
            'salon_id': 1,
            'subject_id': 1,
            'schedule_id': random.choice(schedule_ids),
            'teacher_id': 1,
            'day_of_week_id': random.choice(day_of_week_ids)
        }
        self.classes_factory.get_or_create_class(class_data)

    def generate_classes(self, num_records):
        salon_ids = [salon.id for salon in self.salon_factory.list_salons()]
        subject_ids = [subject.id for subject in self.subject_factory.list_subjects()]
        schedule_ids = [schedule.id for schedule in self.schedule_factory.list_schedules()]
        teacher_ids = [teacher.id for teacher in self.teacher_factory.list_teachers()]
        day_of_week_ids = [day.id for day in self.day_of_week_factory.list_days_of_week()]

        if not salon_ids or not subject_ids or not schedule_ids or not teacher_ids or not day_of_week_ids:
            return
        
        # Primero, generar datos estáticos
        self.generate_static_class()

        for _ in range(num_records):

            class_data = {
                'code': self.fake.unique.lexify(text='????-????'),
                'salon_id': random.choice(salon_ids),
                'subject_id': random.choice(subject_ids),
                'schedule_id': random.choice(schedule_ids),
                'teacher_id': random.choice(teacher_ids),
                'day_of_week_id': random.choice(day_of_week_ids)
            }
            self.classes_factory.get_or_create_class(class_data)

        self.db.commit()