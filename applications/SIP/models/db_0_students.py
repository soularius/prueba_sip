if not 'students' in db.tables:    
    db.define_table('students',
                    Field('uuid', 'string', length=16, unique=True),
                    Field('name', 'string', length=55),
                    Field('lastname', 'string', length=55),
                    Field('phone', 'integer', length=30),
                    Field('email', 'string', length=45, unique=True))

    # validation for 'students'
    db.students.name.requires = IS_NOT_EMPTY()
    db.students.lastname.requires = IS_NOT_EMPTY()
    db.students.email.requires = [IS_NOT_EMPTY(), IS_EMAIL(), IS_NOT_IN_DB(db, 'students.email')]
    db.students.phone.requires = [IS_NOT_EMPTY(), IS_MATCH('^[0-9]{10}$', error_message='Please enter a valid phone number.')]