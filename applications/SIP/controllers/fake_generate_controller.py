from applications.SIP.modules.utils.fake_data_student_generator import FakeDataStudentGenerator
from applications.SIP.modules.utils.fake_data_teacher_generator import FakeDataTeacherGenerator
from applications.SIP.modules.utils.fake_data_schedules_generator import FakeDataScheduleGenerator
from applications.SIP.modules.utils.fake_data_subjects_generator import FakeDataSubjectGenerator
from applications.SIP.modules.utils.fake_data_salons_generator import FakeDataSalonGenerator
from applications.SIP.modules.utils.fake_data_day_of_week_generator import FakeDataDayOfWeekGenerator

from applications.SIP.modules.utils.fake_data_classes_generator import FakeDataClassesGenerator
from applications.SIP.modules.utils.fake_data_classes_students_generator import FakeDataClassesStudentsGenerator
from applications.SIP.modules.utils.fake_data_attendance_generator import FakeDataAttendanceGenerator

class FakeGenerateController:
    def __init__(self, db):
        self.db = db
    
    def index(self):
        """
        Generates fake data for students, teachers, schedules, subjects, salons, classes, class students, and attendance.
        
        :return: A dictionary containing the message "Datos generados exitosamente"
        """
        FakeDataStudentGenerator(self.db).generate_students(50)
        FakeDataTeacherGenerator(self.db).generate_teachers(50)
        FakeDataScheduleGenerator(self.db).generate_schedules(50)
        FakeDataSubjectGenerator(self.db).generate_subjects(50)
        FakeDataSalonGenerator(self.db).generate_salons(50)
        FakeDataDayOfWeekGenerator(self.db).generate_days_of_week()
        FakeDataClassesGenerator(self.db).generate_classes(100)
        FakeDataClassesStudentsGenerator(self.db).generate_classes_students(250)
        FakeDataAttendanceGenerator(self.db).generate_attendance(300)
        return dict(message="Datos generados exitosamente")

    def static_data_generate(self):
        """
        Generates static data for the database.

        This function generates fake data for various tables in the database. It calls several generator functions for different entities such as students, teachers, schedules, subjects, salons, days of the week, classes, class students, and attendance. After generating the data, it returns a dictionary with a success message.

        Parameters:
            self: The instance of the class.

        Returns:
            dict: A dictionary containing a success message.
        """
        FakeDataStudentGenerator(self.db).generate_static_student()
        FakeDataTeacherGenerator(self.db).generate_static_teacher()
        FakeDataScheduleGenerator(self.db).generate_schedules(1)
        FakeDataSubjectGenerator(self.db).generate_static_subject()
        FakeDataSalonGenerator(self.db).generate_static_salon()
        FakeDataDayOfWeekGenerator(self.db).generate_days_of_week()
        FakeDataClassesGenerator(self.db).generate_static_class()
        FakeDataClassesStudentsGenerator(self.db).generate_static_classes_students()
        FakeDataAttendanceGenerator(self.db).generate_static_attendance()
        return dict(message="Datos generados exitosamente")