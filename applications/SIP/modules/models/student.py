from gluon import *
class Student:    
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if not 'students' in self.db.tables:    
            self.db.define_table('students',
                            Field('uuid', 'string', length=16, unique=True),
                            Field('name', 'string', length=55),
                            Field('lastname', 'string', length=55),
                            Field('phone', 'integer', length=30),
                            Field('email', 'string', length=45, unique=True))

            # validation for 'students'
            self.db.students.name.requires = IS_NOT_EMPTY()
            self.db.students.lastname.requires = IS_NOT_EMPTY()
            self.db.students.email.requires = [IS_NOT_EMPTY(), IS_EMAIL(), IS_NOT_IN_DB(self.db, 'students.email')]
            self.db.students.phone.requires = [IS_NOT_EMPTY(), IS_MATCH('^[0-9]{10}$', error_message='Please enter a valid phone number.')]