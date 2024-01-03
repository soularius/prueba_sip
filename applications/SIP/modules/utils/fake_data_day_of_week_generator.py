class FakeDataDayOfWeekGenerator:
    def __init__(self, db):
        self.db = db

    def generate_days_of_week(self):
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for day in days:
            self.db.day_of_week.insert(name=day)
        self.db.commit()
