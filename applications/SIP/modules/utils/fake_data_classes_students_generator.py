import random
import string

class FakeDataClassesStudentsGenerator:
    def __init__(self, db):
        self.db = db

    def generate_classes_students(self, num_records):
        student_ids = self.db(self.db.students.id > 0).select(self.db.students.id)
        class_ids = self.db(self.db.classes.id > 0).select(self.db.classes.id)

        for _ in range(num_records):
            section_name = self.generate_unique_section_name()
            self.db.classes_students.insert(
                section_class=section_name,
                classes_id=random.choice(class_ids).id,
                student_id=random.choice(student_ids).id
            )
        self.db.commit()

    def generate_unique_section_name(self):
        while True:
            section_name = f"{random.choice(string.ascii_uppercase)}{random.randint(1, 99):02d}"
            if not self.db(self.db.classes_students.section_class == section_name).count():
                return section_name