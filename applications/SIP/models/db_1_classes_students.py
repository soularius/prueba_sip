if not 'classes_students' in db.tables:
    db.define_table('classes_students',
                    Field('uuid', 'string', length=16, unique=True),
                    Field('class_uuid', 'reference classes'),
                    Field('student_uuid', 'reference students'))
    
    # Validation for 'classes_students'
    db.classes_students.class_uuid.requires = [IS_IN_DB(db, db.classes.uuid, '%(name)s')]
    db.classes_students.student_uuid.requires = [IS_IN_DB(db, db.students.uuid, '%(name)s')]