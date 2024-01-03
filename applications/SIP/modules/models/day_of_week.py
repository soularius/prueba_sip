from gluon import *
class DayOfWeek:    
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'day_of_week' not in self.db.tables:
            self.db.define_table('day_of_week',
                            Field('name', 'string', length=45))

            # validation for 'day_of_week'
            self.db.day_of_week.name.requires = IS_NOT_EMPTY()

            self.db.day_of_week.name.label = 'Día de la semana'