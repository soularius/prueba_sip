from gluon import *
class Subjects:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'subjects' not in self.db.tables:
            self.db.define_table('subjects',
                            Field('name', 'string', length=55),
                            Field('description', 'text'))

            # Validation for 'subjects'
            self.db.subjects.name.requires = IS_NOT_EMPTY()
            self.db.subjects.description.requires = IS_NOT_EMPTY()

            self.db.subjects.name.label = 'Nombre'
            self.db.subjects.description.label = 'Descripción'