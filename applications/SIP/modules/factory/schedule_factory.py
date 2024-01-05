from .singleton_meta import SingletonMeta

class ScheduleFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        """
        Initializes a new instance of the class.
        
        Parameters:
            db (object): The database object to be used.
        
        Returns:
            None
        """
        self.db = db
        self.cache = {}

    def get_or_create_schedule(self, schedule_data):
        """
        Get or create a schedule based on the provided schedule data.

        Args:
            schedule_data (dict): A dictionary containing the schedule data.

        Returns:
            Schedule: The schedule object that was retrieved or created.
        """
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
        """
        Retrieves a schedule from the cache or the database based on the given schedule ID.

        Parameters:
            schedule_id (int): The ID of the schedule to retrieve.

        Returns:
            dict or None: The retrieved schedule, or None if the schedule does not exist.
        """
        if schedule_id in self.cache:
            return self.cache[schedule_id]

        schedule = self.db.schedules(schedule_id)
        if schedule:
            self.cache[schedule_id] = schedule
            return schedule
        return None

    def update_schedule(self, schedule_id, schedule_data):
        """
        Updates the schedule with the specified ID using the provided data.

        :param schedule_id: The ID of the schedule to update.
        :type schedule_id: int
        :param schedule_data: The data to update the schedule with.
        :type schedule_data: dict
        :return: The updated schedule if it exists, None otherwise.
        :rtype: dict or None
        """
        schedule = self.db.schedules(schedule_id)
        if schedule:
            schedule.update_record(**schedule_data)
            self.db.commit()
            self.cache[schedule_id] = schedule
            return schedule
        return None

    def delete_schedule(self, schedule_id):
        """
        Delete a schedule from the cache and the database.

        Parameters:
            schedule_id (int): The ID of the schedule to be deleted.

        Returns:
            None
        """
        if schedule_id in self.cache:
            del self.cache[schedule_id]

        self.db(self.db.schedules.id == schedule_id).delete()
        self.db.commit()

    def list_schedules(self):
        """
        Retrieve and return a list of all schedules from the database.

        :param self: The instance of the class.
        :return: A list of schedules retrieved from the database.
        """
        schedules = self.db(self.db.schedules).select()
        for schedule in schedules:
            self.cache[schedule.id] = schedule
        return schedules