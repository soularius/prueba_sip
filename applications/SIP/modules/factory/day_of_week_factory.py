from .singleton_meta import SingletonMeta

class DayOfWeekFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_day_of_week(self, day_data):
        """
        Retrieves an existing instance of `DayOfWeek` from the cache or the database based on the provided `name`. If an instance with the same `name` exists in the cache, it is returned immediately. If not, a query is made to the database to check if an instance with the same `name` exists. If found, it is added to the cache and returned. If no instance is found, a new `DayOfWeek` instance is created in the database with the provided `day_data` and added to the cache before being returned.

        :param day_data: A dictionary representing the data of the `DayOfWeek` instance to be retrieved or created.
        :type day_data: dict
        :return: An instance of `DayOfWeek` representing the retrieved or created instance.
        :rtype: DayOfWeek
        """
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
        """
        Get the day of the week from the given day name.

        Parameters:
            day_name (str): The name of the day.

        Returns:
            str or None: The day of the week corresponding to the given day name, or None if it is not found.
        """
        if day_name in self.cache:
            return self.cache[day_name]

        day = self.db(self.db.day_of_week.name == day_name).select().first()
        if day:
            self.cache[day_name] = day
            return day
        return None
    
    def list_days_of_week(self):
        """
        Retrieves a list of all the days of the week from the database.

        Returns:
            list: A list of all the days of the week.

        Note:
            This function uses a cache to improve performance. If the cache is empty,
            the function retrieves the days of the week from the database and stores
            them in the cache for future use.

        """
        if not self.cache:
            days = self.db(self.db.day_of_week).select()
            for day in days:
                self.cache[day.id] = day
        return list(self.cache.values())