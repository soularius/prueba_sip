from .singleton_meta import SingletonMeta

class SubjectFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_subject(self, subject_data):
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
        if subject_id in self.cache:
            return self.cache[subject_id]

        subject = self.db.subjects(subject_id)
        if subject:
            self.cache[subject_id] = subject
            return subject
        return None

    def update_subject(self, subject_id, subject_data):
        subject = self.db.subjects(subject_id)
        if subject:
            subject.update_record(**subject_data)
            self.db.commit()
            self.cache[subject_id] = subject
            return subject
        return None

    def delete_subject(self, subject_id):
        if subject_id in self.cache:
            del self.cache[subject_id]

        self.db(self.db.subjects.id == subject_id).delete()
        self.db.commit()

    def list_subjects(self):
        subjects = self.db(self.db.subjects).select()
        for subject in subjects:
            self.cache[subject.id] = subject
        return subjects