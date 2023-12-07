if not 'attendance' in db.tables:
    db.define_table('attendance',
                    Field('uuid', 'string', length=16, unique=True),
                    Field('student_uuid', 'reference students'),
                    Field('class_uuid', 'reference classes'),
                    Field('date_class', 'date'),
                    Field('status', 'integer'))
    
    # Validation for 'attendance'
    db.attendance.student_uuid.requires = [IS_IN_DB(db, db.students.uuid, '%(name)s')]
    db.attendance.class_uuid.requires = [IS_IN_DB(db, db.classes.uuid, '%(name)s')]
    db.attendance.date_class.requires = [IS_NOT_EMPTY(), IS_DATE()]
    db.attendance.status.requires = [IS_NOT_EMPTY(), IS_INT_IN_RANGE(0, 1)]