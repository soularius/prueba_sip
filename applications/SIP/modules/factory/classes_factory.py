from .singleton_meta import SingletonMeta

class ClassesFactory(metaclass=SingletonMeta):
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def get_or_create_class(self, class_data):
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
        if class_id in self.cache:
            return self.cache[class_id]

        class_obj = self.db.classes(class_id)
        if class_obj:
            self.cache[class_id] = class_obj
            return class_obj
        return None

    def update_class(self, class_id, class_data):
        class_obj = self.db.classes(class_id)
        if class_obj:
            class_obj.update_record(**class_data)
            self.db.commit()
            self.cache[class_id] = class_obj
            return class_obj
        return None

    def delete_class(self, class_id):
        if class_id in self.cache:
            del self.cache[class_id]

        self.db(self.db.classes.id == class_id).delete()
        self.db.commit()

    def list_classes(self):
        classes = self.db(self.db.classes).select()
        for class_obj in classes:
            self.cache[class_obj.id] = class_obj
        return classes