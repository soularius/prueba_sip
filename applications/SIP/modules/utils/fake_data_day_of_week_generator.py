from applications.SIP.modules.factory.day_of_week_factory import DayOfWeekFactory

class FakeDataDayOfWeekGenerator:
    def __init__(self, db):
        self.db = db
        self.day_of_week_factory = DayOfWeekFactory(db)

    def generate_days_of_week(self):
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for day in days:
            day_data = {'name': day}
            self.day_of_week_factory.get_or_create_day_of_week(day_data)

        self.db.commit()
