from gluon import *
class Teachers:
    def __init__(self, db):
        self.db = db
    def define_table(self):
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