from gluon import *
class Schedules:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'schedules' not in self.db.tables:
            self.db.define_table('schedules',
                            Field('block_start', 'time'),
                            Field('block_end', 'time'))

            # validation for 'schedules'
            self.db.schedules.block_start.requires = IS_NOT_EMPTY()
            self.db.schedules.block_end.requires = IS_NOT_EMPTY()