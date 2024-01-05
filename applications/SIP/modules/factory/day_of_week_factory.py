from .singleton_meta import SingletonMeta

class DayOfWeekFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_day_of_week(self, day_data):
        name = day_data.get('name')

        for day_obj in self.cache.values():
            if day_obj.name == name:
                return day_obj
            
        existing_day_data = self.db(self.db.day_of_week.name == name).select().first()
        if existing_day_data:
            self.cache[existing_day_data.id] = existing_day_data
            return existing_day_data
        
        day_of_week_id = self.db.day_of_week.insert(**day_data)
        self.db.commit()

        new_day_of_week_id = self.db.day_of_week(day_of_week_id)
        self.cache[new_day_of_week_id.id] = new_day_of_week_id
        return new_day_of_week_id

    def get_day_of_week(self, day_name):
        if day_name in self.cache:
            return self.cache[day_name]

        day = self.db(self.db.day_of_week.name == day_name).select().first()
        if day:
            self.cache[day_name] = day
            return day
        return None
    
    def list_days_of_week(self):
        if not self.cache:
            days = self.db(self.db.day_of_week).select()
            for day in days:
                self.cache[day.id] = day
        return list(self.cache.values())