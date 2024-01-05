from gluon import *
class Subjects:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        """
        Defines the 'subjects' table in the database if it does not already exist.
        
        This function creates the 'subjects' table with the following fields:
        - name: string, length=55, required
        - description: text, required
        
        The 'name' and 'description' fields are validated to ensure they are not empty.
        
        The labels for the 'name' and 'description' fields are set to 'Nombre' and 'Descripción' respectively.
        """
        if 'subjects' not in self.db.tables:
            self.db.define_table('subjects',
                            Field('name', 'string', length=55, required=True),
                            Field('description', 'text', required=True))

            # Validation for 'subjects'
            self.db.subjects.name.requires = IS_NOT_EMPTY()
            self.db.subjects.description.requires = IS_NOT_EMPTY()

            self.db.subjects.name.label = 'Nombre'
            self.db.subjects.description.label = 'Descripción'