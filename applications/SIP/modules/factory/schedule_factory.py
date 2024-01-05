from .singleton_meta import SingletonMeta

class ScheduleFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_schedule(self, schedule_data):
        block_start = schedule_data.get('block_start')
        block_end = schedule_data.get('block_end')

        # Primero verificar en la caché
        for schedule in self.cache.values():
            if schedule.block_start == block_start and schedule.block_end == block_end:
                return schedule

        # Verificar en la base de datos
        existing_schedule = self.db((self.db.schedules.block_start == block_start) & 
                                    (self.db.schedules.block_end == block_end)).select().first()
        if existing_schedule:
            self.cache[existing_schedule.id] = existing_schedule
            return existing_schedule

        # Si no existe, crear un nuevo horario
        schedule_id = self.db.schedules.insert(**schedule_data)
        self.db.commit()

        # Recuperar y cachear el objeto horario insertado
        new_schedule = self.db.schedules(schedule_id)
        self.cache[new_schedule.id] = new_schedule
        return new_schedule

    def get_schedule(self, schedule_id):
        if schedule_id in self.cache:
            return self.cache[schedule_id]

        schedule = self.db.schedules(schedule_id)
        if schedule:
            self.cache[schedule_id] = schedule
            return schedule
        return None

    def update_schedule(self, schedule_id, schedule_data):
        schedule = self.db.schedules(schedule_id)
        if schedule:
            schedule.update_record(**schedule_data)
            self.db.commit()
            self.cache[schedule_id] = schedule
            return schedule
        return None

    def delete_schedule(self, schedule_id):
        if schedule_id in self.cache:
            del self.cache[schedule_id]

        self.db(self.db.schedules.id == schedule_id).delete()
        self.db.commit()

    def list_schedules(self):
        schedules = self.db(self.db.schedules).select()
        for schedule in schedules:
            self.cache[schedule.id] = schedule
        return schedules