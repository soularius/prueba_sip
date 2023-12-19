from gluon import *
class Classes:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'classes' not in self.db.tables:
            self.db.define_table('classes',
                            Field('salon_id', 'reference salons', ondelete='CASCADE'),
                            Field('subject_id', 'reference subjects', ondelete='CASCADE'),
                            Field('schedule_id', 'reference schedules', ondelete='CASCADE'),
                            Field('teacher_id', 'reference teachers', ondelete='CASCADE'),
                            Field('day_of_week_id', 'reference day_of_week', ondelete='CASCADE'))
            
            # Validation for 'classes'
            self.db.classes.salon_id.requires = [IS_IN_DB(self.db, self.db.salons.id, '%(name)s')]
            self.db.classes.subject_id.requires = [IS_IN_DB(self.db, self.db.subjects.id, '%(name)s')]
            self.db.classes.schedule_id.requires = [IS_IN_DB(self.db, self.db.schedules.id, '%(name)s')]
            self.db.classes.teacher_id.requires = [IS_IN_DB(self.db, self.db.teachers.id, '%(name)s')]
            self.db.classes.day_of_week_id.requires = [IS_IN_DB(self.db, self.db.day_of_week.id, '%(name)s')]