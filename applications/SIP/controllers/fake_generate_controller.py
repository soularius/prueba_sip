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
