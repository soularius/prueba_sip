from gluon import *
class Teachers:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        """
        Defines the 'teachers' table in the database.

        This function checks if the 'teachers' table does not exist in the database, and if not, it defines the table with the following fields:
        - 'name' (string, length=55, required=True)
        - 'lastname' (string, length=55, required=True)
        - 'phone' (string, length=55, required=True)
        - 'email' (string, length=45, unique=True, required=True)

        The function also adds validation for each field:
        - 'name' requires a non-empty value
        - 'lastname' requires a non-empty value
        - 'email' requires a non-empty value, a valid email format, and should not already exist in the 'teachers' table
        - 'phone' requires a non-empty value and should match the pattern '^[0-9]{10}$' (10-digit format)

        Additionally, the function sets labels for each field:
        - 'name' label is set to 'Nombre'
        - 'lastname' label is set to 'Apellido'
        - 'email' label is set to 'Correo Electrónico'
        - 'phone' label is set to 'Teléfono'
        """
        if 'teachers' not in self.db.tables:
            self.db.define_table('teachers',
                            Field('name', 'string', length=55, required=True),
                            Field('lastname', 'string', length=55, required=True),
                            Field('phone', 'string', length=55, required=True),
                            Field('email', 'string', length=45, unique=True, required=True))

            # Validation for 'teachers'
            self.db.teachers.name.requires = IS_NOT_EMPTY()
            self.db.teachers.lastname.requires = IS_NOT_EMPTY()
            self.db.teachers.email.requires = [IS_NOT_EMPTY(), IS_EMAIL(), IS_NOT_IN_DB(self.db, 'teachers.email')]
            self.db.teachers.phone.requires = [IS_NOT_EMPTY(), IS_MATCH('^[0-9]{10}$', error_message='Please enter a valid phone number.')]

            self.db.teachers.name.label = 'Nombre'
            self.db.teachers.lastname.label = 'Apellido'
            self.db.teachers.email.label = 'Correo Electrónico'
            self.db.teachers.phone.label = 'Teléfono'