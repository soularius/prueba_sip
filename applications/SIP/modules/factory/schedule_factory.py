from .singleton_meta import SingletonMeta

class ScheduleFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_schedule(self, id, block_start, block_end):
        if id not in self.cache:
            schedule = self.db.schedules.insert(id=id, block_start=block_start, block_end=block_end)
            self.cache[id] = schedule
        return self.cache[id]