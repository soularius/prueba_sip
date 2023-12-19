from gluon import *
class Attendance:    
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'attendance' not in self.db.tables:
            self.db.define_table('attendance',
                            Field('student_id', 'reference students', ondelete='CASCADE'),
                            Field('class_id', 'reference classes', ondelete='CASCADE'),
                            Field('date_class', 'date'),
                            Field('status', 'integer'))
            
            # Validation for 'attendance'
            self.db.attendance.student_id.requires = [IS_IN_DB(self.db, self.db.students.id, '%(name)s')]
            self.db.attendance.class_id.requires = [IS_IN_DB(self.db, self.db.classes.id, '%(name)s')]
            self.db.attendance.date_class.requires = [IS_NOT_EMPTY(), IS_DATE()]
            self.db.attendance.status.requires = [IS_NOT_EMPTY(), IS_INT_IN_RANGE(0, 1)]