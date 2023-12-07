db.define_table('classes_students',
                Field('uuid', 'string', length=16, unique=True),
                Field('class_uuid', 'reference classes'),
                Field('student_uuid', 'reference students'))