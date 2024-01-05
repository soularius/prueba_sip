from gluon import *
class Salons:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'salons' not in self.db.tables:
            self.db.define_table('salons',
                            Field('name', 'string', length=45, required=True),
                            Field('description', 'text', required=True))

            # Validation for 'salons'
            self.db.salons.name.requires = IS_NOT_EMPTY()
            self.db.salons.description.requires = IS_NOT_EMPTY()

            self.db.salons.name.label = 'Nombre'
            self.db.salons.description.label = 'Descripción'