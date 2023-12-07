from .singleton_meta import SingletonMeta

class DayOfWeekFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_day_of_week(self, uuid, name):
        if uuid not in self.cache:
            day_of_week = db.day_of_week.insert(uuid=uuid, name=name)
            self.cache[uuid] = day_of_week
        return self.cache[uuid]