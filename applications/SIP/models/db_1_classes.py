if not 'classes' in db.tables:
    db.define_table('classes',
                    Field('uuid', 'string', length=16, unique=True),
                    Field('salon_uuid', 'reference salons'),
                    Field('subject_uuid', 'reference subjects'),
                    Field('schedule_uuid', 'reference schedules'),
                    Field('teacher_uuid', 'reference teachers'),
                    Field('day_of_week_uuid', 'reference day_of_week'))
    
    # Validation for 'classes'
    db.classes.salon_uuid.requires = [IS_IN_DB(db, db.salons.uuid, '%(name)s')]
    db.classes.subject_uuid.requires = [IS_IN_DB(db, db.subjects.uuid, '%(name)s')]
    db.classes.schedule_uuid.requires = [IS_IN_DB(db, db.schedules.uuid, '%(name)s')]
    db.classes.teacher_uuid.requires = [IS_IN_DB(db, db.teachers.uuid, '%(name)s')]
    db.classes.day_of_week_uuid.requires = [IS_IN_DB(db, db.day_of_week.uuid, '%(name)s')]