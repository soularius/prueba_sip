from .singleton_meta import SingletonMeta

class ClassesFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        """
        Initializes the class instance with a given database.

        Parameters:
            db (Database): The database to be used.

        Returns:
            None
        """
        self.db = db
        self.cache = {}

    def get_or_create_class(self, class_data):
        """
        Retrieves an existing class object from the cache or the database based on the provided class code. If the class object exists in the cache, it is returned. If not, the database is queried to check if the class object exists. If the class object is found in the database, it is added to the cache and returned. If the class object is not found in the cache or database, a new class object is created in the database, added to the cache, and returned.

        Parameters:
            class_data (dict): A dictionary containing the data of the class to be retrieved or created. It should include the 'code' key with the code of the class.

        Returns:
            Class: The retrieved or created class object.

        """
        code = class_data.get('code')
        for class_obj in self.cache.values():
            if class_obj.code == code:
                return class_obj
            
        existing_class = self.db(self.db.classes.code == code).select().first()
        if existing_class:
            self.cache[existing_class.id] = existing_class
            return existing_class
        
        class_id = self.db.classes.insert(**class_data)
        self.db.commit()

        new_class = self.db.classes(class_id)
        self.cache[new_class.id] = new_class
        return new_class

    def get_class(self, class_id):
        """
        Retrieves a class object based on the given class ID.

        Parameters:
            class_id (int): The ID of the class to retrieve.

        Returns:
            class_obj (Class): The class object corresponding to the given class ID, if found. Otherwise, None.
        """
        if class_id in self.cache:
            return self.cache[class_id]

        class_obj = self.db.classes(class_id)
        if class_obj:
            self.cache[class_id] = class_obj
            return class_obj
        return None

    def update_class(self, class_id, class_data):
        """
        Updates a class record in the database.

        Args:
            class_id (str): The ID of the class to update.
            class_data (dict): The updated data for the class.

        Returns:
            ClassObject or None: The updated class object if it exists, None otherwise.
        """
        class_obj = self.db.classes(class_id)
        if class_obj:
            class_obj.update_record(**class_data)
            self.db.commit()
            self.cache[class_id] = class_obj
            return class_obj
        return None

    def delete_class(self, class_id):
        """
        Deletes a class from the cache and the database.

        Parameters:
            class_id (int): The ID of the class to be deleted.

        Returns:
            None
        """
        if class_id in self.cache:
            del self.cache[class_id]

        self.db(self.db.classes.id == class_id).delete()
        self.db.commit()

    def list_classes(self):
        """
        Retrieves a list of all classes from the database.

        Parameters:
            self (ClassName): An instance of the ClassName class.

        Returns:
            classes (list): A list of class objects retrieved from the database.
        """
        classes = self.db(self.db.classes).select()
        for class_obj in classes:
            self.cache[class_obj.id] = class_obj
        return classes