from gluon import *
class Attendance:    
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if not 'attendance' in self.db.tables:
            self.db.define_table('attendance',
                            Field('uuid', 'string', length=16, unique=True),
                            Field('student_uuid', 'reference students'),
                            Field('class_uuid', 'reference classes'),
                            Field('date_class', 'date'),
                            Field('status', 'integer'))
            
            # Validation for 'attendance'
            self.db.attendance.student_uuid.requires = [IS_IN_DB(self.db, self.db.students.uuid, '%(name)s')]
            self.db.attendance.class_uuid.requires = [IS_IN_DB(self.db, self.db.classes.uuid, '%(name)s')]
            self.db.attendance.date_class.requires = [IS_NOT_EMPTY(), IS_DATE()]
            self.db.attendance.status.requires = [IS_NOT_EMPTY(), IS_INT_IN_RANGE(0, 1)]