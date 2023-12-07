from gluon import *
class Classes:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if not 'classes' in self.db.tables:
            self.db.define_table('classes',
                            Field('uuid', 'string', length=16, unique=True),
                            Field('salon_uuid', 'reference salons'),
                            Field('subject_uuid', 'reference subjects'),
                            Field('schedule_uuid', 'reference schedules'),
                            Field('teacher_uuid', 'reference teachers'),
                            Field('day_of_week_uuid', 'reference day_of_week'))
            
            # Validation for 'classes'
            self.db.classes.salon_uuid.requires = [IS_IN_DB(self.db, self.db.salons.uuid, '%(name)s')]
            self.db.classes.subject_uuid.requires = [IS_IN_DB(self.db, self.db.subjects.uuid, '%(name)s')]
            self.db.classes.schedule_uuid.requires = [IS_IN_DB(self.db, self.db.schedules.uuid, '%(name)s')]
            self.db.classes.teacher_uuid.requires = [IS_IN_DB(self.db, self.db.teachers.uuid, '%(name)s')]
            self.db.classes.day_of_week_uuid.requires = [IS_IN_DB(self.db, self.db.day_of_week.uuid, '%(name)s')]