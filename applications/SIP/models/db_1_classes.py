db.define_table('classes',
                Field('uuid', 'string', length=16, unique=True),
                Field('salon', 'reference salons'),
                Field('subject', 'reference subjects'),
                Field('schedule', 'reference schedules'),
                Field('teacher', 'reference teachers'),
                Field('day_of_week', 'reference day_of_week'))