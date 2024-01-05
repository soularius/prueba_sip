from .singleton_meta import SingletonMeta

class SalonFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        """
        Initializes an instance of the class.

        Args:
            db (Database): The database object to be used.

        Returns:
            None
        """
        self.db = db
        self.cache = {}

    def get_or_create_salon(self, salon_data):
        """
        Retrieves an existing salon from the cache or the database based on the provided salon data. If no existing salon is found, a new salon is created in the database and added to the cache.

        Parameters:
            salon_data (dict): A dictionary representing the salon data, including the 'name' of the salon.

        Returns:
            Salon: The retrieved or newly created salon object.
        """
        name = salon_data.get('name')

        for salon in self.cache.values():
            if salon.name == name:
                return salon

        existing_salon = self.db(self.db.salons.name == name).select().first()
        if existing_salon:
            self.cache[existing_salon.id] = existing_salon
            return existing_salon

        salon_id = self.db.salons.insert(**salon_data)
        self.db.commit()

        new_salon = self.db.salons(salon_id)
        self.cache[new_salon.id] = new_salon
        return new_salon

    def get_salon(self, salon_id):
        """
        Retrieves a salon from the cache or the database.

        Parameters:
            salon_id (int): The ID of the salon to retrieve.

        Returns:
            Salon or None: The retrieved salon if found, or None if not found.
        """
        if salon_id in self.cache:
            return self.cache[salon_id]

        salon = self.db.salons(salon_id)
        if salon:
            self.cache[salon_id] = salon
            return salon
        return None

    def update_salon(self, salon_id, salon_data):
        """
        Updates the data of a salon in the database.

        Parameters:
            salon_id (int): The ID of the salon to be updated.
            salon_data (dict): The updated data for the salon.

        Returns:
            Salon: The updated salon object if it exists in the database, None otherwise.
        """
        salon = self.db.salons(salon_id)
        if salon:
            salon.update_record(**salon_data)
            self.db.commit()
            self.cache[salon_id] = salon
            return salon
        return None

    def delete_salon(self, salon_id):
        """
        Deletes a salon from the cache and the database.

        Parameters:
            salon_id (int): The ID of the salon to be deleted.

        Returns:
            None
        """
        if salon_id in self.cache:
            del self.cache[salon_id]

        self.db(self.db.salons.id == salon_id).delete()
        self.db.commit()

    def list_salons(self):
        """
        Retrieves a list of all salons from the database.

        :param self: The current instance of the class.
        :return: A list of salon objects representing all salons in the database.
        """
        salons = self.db(self.db.salons).select()
        for salon in salons:
            self.cache[salon.id] = salon
        return salons