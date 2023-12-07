from .singleton_meta import SingletonMeta

class ScheduleFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def create_schedule(self, uuid, block_start, block_end):
        if uuid not in self.cache:
            schedule = db.schedules.insert(uuid=uuid, block_start=block_start, block_end=block_end)
            self.cache[uuid] = schedule
        return self.cache[uuid]