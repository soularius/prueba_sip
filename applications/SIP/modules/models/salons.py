from gluon import *
class Salons:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        """
        Define the 'salons' table if it does not already exist in the database.

        This function creates the 'salons' table in the database, with the following fields:
        - 'name': a string field with a maximum length of 45 characters, which is required.
        - 'description': a text field, which is also required.

        The function also adds validation rules for the 'name' and 'description' fields:
        - The 'name' field must not be empty.
        - The 'description' field must not be empty.

        Additionally, the function sets labels for the 'name' and 'description' fields:
        - The label for the 'name' field is set to 'Nombre'.
        - The label for the 'description' field is set to 'Descripción'.
        """
        if 'salons' not in self.db.tables:
            self.db.define_table('salons',
                            Field('name', 'string', length=45, required=True),
                            Field('description', 'text', required=True))

            # Validation for 'salons'
            self.db.salons.name.requires = IS_NOT_EMPTY()
            self.db.salons.description.requires = IS_NOT_EMPTY()

            self.db.salons.name.label = 'Nombre'
            self.db.salons.description.label = 'Descripción'