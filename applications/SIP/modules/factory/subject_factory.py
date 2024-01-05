from .singleton_meta import SingletonMeta

class SubjectFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        """
        Initializes a new instance of the class.

        Parameters:
            db (Database): The database object to be used.

        Returns:
            None
        """
        self.db = db
        self.cache = {}

    def get_or_create_subject(self, subject_data):
        """
        Retrieves an existing subject from the cache or the database based on the provided subject data. If the subject does not exist, a new subject is created in the database.
        
        Args:
            subject_data (dict): A dictionary containing the subject data, including the 'name' key.
        
        Returns:
            Subject: The retrieved or newly created subject object.
        """
        name = subject_data.get('name')

        for subject in self.cache.values():
            if subject.name == name:
                return subject

        existing_subject = self.db(self.db.subjects.name == name).select().first()
        if existing_subject:
            self.cache[existing_subject.id] = existing_subject
            return existing_subject

        subject_id = self.db.subjects.insert(**subject_data)
        self.db.commit()

        new_subject = self.db.subjects(subject_id)
        self.cache[new_subject.id] = new_subject
        return new_subject

    def get_subject(self, subject_id):
        """
        Retrieves a subject from the cache or the database based on the given subject ID.

        Parameters:
            subject_id (int): The ID of the subject to retrieve.

        Returns:
            subject (Subject or None): The retrieved subject object if found, or None if not found.
        """
        if subject_id in self.cache:
            return self.cache[subject_id]

        subject = self.db.subjects(subject_id)
        if subject:
            self.cache[subject_id] = subject
            return subject
        return None

    def update_subject(self, subject_id, subject_data):
        """
        Update a subject in the database with the given subject ID and subject data.

        :param subject_id: The ID of the subject to be updated.
        :type subject_id: int
        :param subject_data: The updated data for the subject.
        :type subject_data: dict
        :return: The updated subject if it exists, otherwise None.
        :rtype: dict or None
        """
        subject = self.db.subjects(subject_id)
        if subject:
            subject.update_record(**subject_data)
            self.db.commit()
            self.cache[subject_id] = subject
            return subject
        return None

    def delete_subject(self, subject_id):
        """
        Delete a subject from the cache and the database.

        Args:
            subject_id (int): The ID of the subject to be deleted.

        Returns:
            None
        """
        if subject_id in self.cache:
            del self.cache[subject_id]

        self.db(self.db.subjects.id == subject_id).delete()
        self.db.commit()

    def list_subjects(self):
        """
        Retrieves a list of subjects from the database.

        Parameters:
            self (obj): The instance of the current class.

        Returns:
            list: A list of subjects retrieved from the database.
        """
        subjects = self.db(self.db.subjects).select()
        for subject in subjects:
            self.cache[subject.id] = subject
        return subjects