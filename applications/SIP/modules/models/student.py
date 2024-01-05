from gluon import *
class Student:    
    def __init__(self, db):
        self.db = db
    def define_table(self):
        """
        Defines the 'students' table in the database.

        This function checks if the 'students' table already exists in the database. If it does not exist,
        it defines the table with the following fields:
        - 'name': string, length=55, required=True
        - 'lastname': string, length=55, required=True
        - 'phone': string, length=55, required=True
        - 'email': string, length=55, unique=True, required=True

        The function then sets up the validation requirements for each field:
        - 'name': IS_NOT_EMPTY()
        - 'lastname': IS_NOT_EMPTY()
        - 'email': IS_NOT_EMPTY(), IS_EMAIL(), IS_NOT_IN_DB(self.db, 'students.email')
        - 'phone': IS_NOT_EMPTY(), IS_MATCH('^[0-9]{10}$', error_message='Please enter a valid phone number.')

        Additionally, the function sets up the labels for each field:
        - 'name': 'Nombre'
        - 'lastname': 'Apellido'
        - 'email': 'Correo Electrónico'
        - 'phone': 'Teléfono'
        """
        if 'students' not in self.db.tables:
            self.db.define_table('students',
                                 Field('name', 'string', length=55, required=True),
                                 Field('lastname', 'string', length=55, required=True),
                                 Field('phone', 'string', length=55, required=True),
                                 Field('email', 'string', length=55, unique=True, required=True))

            # validation for 'students'
            self.db.students.name.requires = IS_NOT_EMPTY()
            self.db.students.lastname.requires = IS_NOT_EMPTY()
            self.db.students.email.requires = [IS_NOT_EMPTY(), IS_EMAIL(), IS_NOT_IN_DB(self.db, 'students.email')]
            self.db.students.phone.requires = [IS_NOT_EMPTY(), IS_MATCH('^[0-9]{10}$', error_message='Please enter a valid phone number.')]

            self.db.students.name.label = 'Nombre'
            self.db.students.lastname.label = 'Apellido'
            self.db.students.email.label = 'Correo Electrónico'
            self.db.students.phone.label = 'Teléfono'