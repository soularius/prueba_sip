from .singleton_meta import SingletonMeta

class DayOfWeekFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_day_of_week(self, id, name):
        if id not in self.cache:
            day_of_week = self.db.day_of_week.insert(id=id, name=name)
            self.cache[id] = day_of_week
        return self.cache[id]