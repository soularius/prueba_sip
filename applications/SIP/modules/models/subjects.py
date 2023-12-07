from gluon import *
class Subjects:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if not 'subjects' in self.db.tables:
            self.db.define_table('subjects',
                            Field('uuid', 'string', length=16, unique=True),
                            Field('name', 'string', length=55),
                            Field('description', 'text'))

            # Validation for 'subjects'
            self.db.subjects.name.requires = IS_NOT_EMPTY()
            self.db.subjects.description.requires = IS_NOT_EMPTY()