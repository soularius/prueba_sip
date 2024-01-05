from .singleton_meta import SingletonMeta

class TeacherFactory(metaclass=SingletonMeta):
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

    def get_or_create_teacher(self, teacher_data):
        """
        Retrieves an existing teacher from the cache or the database based on the provided teacher data.
        
        Parameters:
            teacher_data (dict): A dictionary containing the teacher data.
        
        Returns:
            Teacher: The retrieved or created Teacher object.
        """
        email = teacher_data.get('email')

        for teacher in self.cache.values():
            if teacher.email == email:
                return teacher

        existing_teacher = self.db(self.db.teachers.email == email).select().first()
        if existing_teacher:
            self.cache[existing_teacher.id] = existing_teacher
            return existing_teacher

        teacher_id = self.db.teachers.insert(**teacher_data)
        self.db.commit()

        new_teacher = self.db.teachers(teacher_id)
        self.cache[new_teacher.id] = new_teacher
        return new_teacher

    def get_teacher(self, teacher_id):
        """
        Retrieves a teacher from the database based on the given teacher ID.
        
        Args:
            teacher_id (int): The ID of the teacher to retrieve.
        
        Returns:
            Teacher or None: The retrieved teacher object if found, None otherwise.
        """
        if teacher_id in self.cache:
            return self.cache[teacher_id]

        teacher = self.db.teachers(teacher_id)
        if teacher:
            self.cache[teacher_id] = teacher
            return teacher
        return None

    def update_teacher(self, teacher_id, teacher_data):
        """
        Updates the information of a teacher in the database.

        Args:
            teacher_id (int): The ID of the teacher to update.
            teacher_data (dict): A dictionary containing the updated data for the teacher.

        Returns:
            Teacher or None: The updated Teacher object if the teacher was found and updated successfully,
            None otherwise.
        """
        teacher = self.db.teachers(teacher_id)
        if teacher:
            teacher.update_record(**teacher_data)
            self.db.commit()
            self.cache[teacher_id] = teacher
            return teacher
        return None

    def delete_teacher(self, teacher_id):
        """
        Deletes a teacher from the cache and the database.

        Parameters:
            teacher_id (int): The ID of the teacher to be deleted.

        Returns:
            None
        """
        if teacher_id in self.cache:
            del self.cache[teacher_id]

        self.db(self.db.teachers.id == teacher_id).delete()
        self.db.commit()

    def list_teachers(self):
        """
        Retrieves a list of teachers from the database.

        Returns:
            List: A list of teacher objects representing each teacher in the database.
        """
        teachers = self.db(self.db.teachers).select()
        for teacher in teachers:
            self.cache[teacher.id] = teacher
        return teachers
