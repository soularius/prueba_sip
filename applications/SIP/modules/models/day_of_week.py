from gluon import *
class DayOfWeek:    
    def __init__(self, db):
        self.db = db
    def define_table(self):    
        if not 'day_of_week' in self.db.tables:     
            self.db.define_table('day_of_week',
                            Field('uuid', 'string', length=16, unique=True),
                            Field('name', 'string', length=45))

            # validation for 'day_of_week'
            self.db.day_of_week.name.requires = IS_NOT_EMPTY()