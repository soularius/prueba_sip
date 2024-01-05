from .singleton_meta import SingletonMeta

class StudentFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        """
        Initializes a new instance of the class.

        Args:
            db (object): The database object.

        Returns:
            None
        """
        self.db = db
        self.cache = {}

    def get_or_create_student(self, student_data):
        """
        Retrieves an existing student from the cache or the database based on the provided student data. If no existing student is found, a new student is created in the database.

        Args:
            student_data (dict): A dictionary containing the data of the student to be retrieved or created. The dictionary should include the 'email' key.

        Returns:
            student (Student): The retrieved or created student object.

        Raises:
            None
        """
        email = student_data.get('email')
        for student in self.cache.values():
            if student.email == email:
                return student
            
        existing_student = self.db(self.db.students.email == email).select().first()
        if existing_student:
            self.cache[existing_student.id] = existing_student
            return existing_student
        
        student_id = self.db.students.insert(**student_data)
        self.db.commit()

        new_student = self.db.students(student_id)
        self.cache[new_student.id] = new_student
        return new_student

    def update_student(self, student_id, student_data):
        """
        Updates a student record with new data.

        Parameters:
            student_id (int): The ID of the student to be updated.
            student_data (dict): A dictionary containing the updated data for the student.

        Returns:
            student (dict): The updated student record if the student exists in the database.
            None: If the student does not exist in the database.
        """
        student = self.db.students(student_id)
        if student:
            student.update_record(**student_data)
            self.db.commit()
            self.cache[student_id] = student
            return student
        return None

    def delete_student(self, student_id):
        """
        Deletes a student from the cache and the database.

        Parameters:
            student_id (int): The ID of the student to be deleted.

        Returns:
            None
        """
        if student_id in self.cache:
            del self.cache[student_id]

        self.db(self.db.students.id == student_id).delete()
        self.db.commit()

    def get_student(self, student_id):
        """
        Retrieves a student from the cache or the database.

        Parameters:
            student_id (int): The ID of the student to retrieve.

        Returns:
            student (dict): The student information if found in the cache or the database, otherwise None.
        """
        if student_id in self.cache:
            return self.cache[student_id]

        student = self.db.students(student_id)
        if student:
            self.cache[student_id] = student
            return student
        return None

    def list_students(self, page, items_per_page):
        """
        Retrieves a list of students from the database, based on the given page and items per page.

        Parameters:
            page (int): The page number to retrieve.
            items_per_page (int): The number of items to retrieve per page.

        Returns:
            list: A list of student records.

        Raises:
            None
        """
        start = (page - 1) * items_per_page
        end = page * items_per_page
        students = self.db(self.db.students).select(orderby=self.db.students.id, limitby=(start, end))
        for student in students:
            self.cache[student.id] = student
        return students