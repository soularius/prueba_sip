import random
import string
from applications.SIP.modules.factory.classes_students_factory import ClassesStudentsFactory

class FakeDataClassesStudentsGenerator:
    def __init__(self, db):
            self.db = db
            self.classes_students_factory = ClassesStudentsFactory(db)

    def generate_static_classes_students(self):
        """
        Generate static classes students.

        This function generates a static student for a specific class section. If there is no existing
        record for the class section "A45T HOUSTON" in the classes_students table, a new record is created.
        The generated student is assigned the following information:
        - id: 1
        - section_class: "A45T HOUSTON"
        - classes_id: 1
        - student_id: 1

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        # Generar un estudiante estático
        if not self.db(self.db.classes_students.section_class == "A45T HOUSTON").select().first():
            classes_student_data = {
                'id': 1,
                'section_class': "A45T HOUSTON",
                'classes_id': 1,
                'student_id': 1
            }
            self.classes_students_factory.get_or_create_classes_student(classes_student_data)

    def generate_classes_students(self, num_records):
        """
        Generates classes and students records.

        Args:
            num_records (int): The number of records to generate.

        Returns:
            None
        """
        student_ids = [student.id for student in self.db(self.db.students.id > 0).select()]
        class_ids = [class_obj.id for class_obj in self.db(self.db.classes.id > 0).select()]

        if not student_ids or not class_ids:
            return
        
        for _ in range(num_records):
            section_name = self.generate_unique_section_name()
            classes_student_data = {
                'section_class': section_name,
                'classes_id': random.choice(class_ids),
                'student_id': random.choice(student_ids)
            }
            self.classes_students_factory.get_or_create_classes_student(classes_student_data)

        self.db.commit()

    def generate_unique_section_name(self):
        """
        Generate a unique section name.

        Returns:
            str: A unique section name.
        """
        while True:
            section_name = f"{random.choice(string.ascii_uppercase)}{random.randint(1, 99):02d}"
            if not self.db(self.db.classes_students.section_class == section_name).count():
                return section_name