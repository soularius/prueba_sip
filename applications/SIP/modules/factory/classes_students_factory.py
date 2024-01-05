from .singleton_meta import SingletonMeta

class ClassesStudentsFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        """
        Initializes a new instance of the class.

        Args:
            db (object): The database object to be assigned to the `db` instance variable.

        Returns:
            None
        """
        self.db = db
        self.cache = {}

    def get_or_create_classes_student(self, classes_student_data):
        """
        Retrieves the class student object based on the provided `classes_student_data` dictionary.

        Args:
            classes_student_data (dict): A dictionary containing the data of the class student.

        Returns:
            ClassStudent: The class student object if found. Otherwise, a new class student object is created and returned.
        """
        section_class_student = classes_student_data.get('section_class')
        for class_student_obj in self.cache.values():
            if class_student_obj.section_class == section_class_student:
                return class_student_obj
            
        existing_class_student = self.db(self.db.classes_students.section_class == section_class_student).select().first()
        if existing_class_student:
            self.cache[existing_class_student.id] = existing_class_student
            return existing_class_student
        
        class_id = self.db.classes_students.insert(**classes_student_data)
        self.db.commit()

        new_class_student = self.db.classes_students(class_id)
        self.cache[new_class_student.id] = new_class_student
        return new_class_student

    def get_classes_student(self, classes_student_id):
        """
        Retrieves the classes_student information for the given classes_student_id.

        Parameters:
            classes_student_id (int): The unique identifier of the classes_student.

        Returns:
            dict: A dictionary containing the classes_student information if found, 
                  None otherwise.
        """
        if classes_student_id in self.cache:
            return self.cache[classes_student_id]

        classes_student = self.db.classes_students(classes_student_id)
        if classes_student:
            self.cache[classes_student_id] = classes_student
            return classes_student
        return None

    def update_classes_student(self, classes_student_id, classes_student_data):
        """
        Update the classes_student record with the given classes_student_id.

        :param classes_student_id: The ID of the classes_student record to update.
        :type classes_student_id: int

        :param classes_student_data: The data to update the classes_student record with.
        :type classes_student_data: dict

        :return: The updated classes_student record if it exists, otherwise None.
        :rtype: dict or None
        """
        classes_student = self.db.classes_students(classes_student_id)
        if classes_student:
            classes_student.update_record(**classes_student_data)
            self.db.commit()
            self.cache[classes_student_id] = classes_student
            return classes_student
        return None

    def delete_classes_student(self, classes_student_id):
        """
        Deletes a classes_student record from the cache and the database.

        Parameters:
            classes_student_id (int): The ID of the classes_student record to be deleted.

        Returns:
            None
        """
        if classes_student_id in self.cache:
            del self.cache[classes_student_id]

        self.db(self.db.classes_students.id == classes_student_id).delete()
        self.db.commit()

    def list_classes_students(self):
        """
        Retrieves a list of all classes and their associated students.

        :param self: The instance of the current object.
        :return: A list of dictionaries representing the classes and their associated students.
        """
        classes_students = self.db(self.db.classes_students).select()
        for classes_student in classes_students:
            self.cache[classes_student.id] = classes_student
        return classes_students