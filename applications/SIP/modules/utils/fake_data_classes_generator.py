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
        """
        Generate a static class.

        This function generates a static class if a class with the code "A01" does not already exist in the database.
        It retrieves a list of schedule IDs and a list of day of week IDs using the respective factory classes.
        It then generates class data with a static ID of 1, code "A01", salon ID of 1, subject ID of 1, a random schedule ID, teacher ID of 1, and a random day of week ID.
        Finally, it calls the classes_factory.get_or_create_class() method to create the class in the database if it does not already exist.

        Parameters:
        - self: The instance of the current class.

        Return:
        - None
        """
        if not self.db(self.db.classes.code == "A01").select().first():
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
        """
        Generate classes with random data.

        This function generates a specified number of classes with random data. It takes in the following parameters:
        - num_records: An integer representing the number of classes to generate.

        The function starts by retrieving the IDs of all salons, subjects, schedules, teachers, and days of the week using their respective factory classes. If any of these lists are empty, the function returns without generating any classes.

        For each iteration in the range of `num_records`, the function creates a dictionary `class_data` with the following keys:
        - 'code': A randomly generated string in the format '????-????'.
        - 'salon_id': A randomly chosen salon ID from the list of salon IDs.
        - 'subject_id': A randomly chosen subject ID from the list of subject IDs.
        - 'schedule_id': A randomly chosen schedule ID from the list of schedule IDs.
        - 'teacher_id': A randomly chosen teacher ID from the list of teacher IDs.
        - 'day_of_week_id': A randomly chosen day of the week ID from the list of day of the week IDs.

        The function then calls the `get_or_create_class()` method of the `classes_factory` object, passing in the `class_data` dictionary as an argument. This method creates a new class instance with the provided data if it does not already exist.

        Finally, the function commits the changes made to the database.

        The function does not return any values.
        """
        salon_ids = [salon.id for salon in self.salon_factory.list_salons()]
        subject_ids = [subject.id for subject in self.subject_factory.list_subjects()]
        schedule_ids = [schedule.id for schedule in self.schedule_factory.list_schedules()]
        teacher_ids = [teacher.id for teacher in self.teacher_factory.list_teachers()]
        day_of_week_ids = [day.id for day in self.day_of_week_factory.list_days_of_week()]

        if not salon_ids or not subject_ids or not schedule_ids or not teacher_ids or not day_of_week_ids:
            return

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