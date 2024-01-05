from gluon import *
from gluon.sqlhtml import TimeWidget
class Schedules:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        """
        Defines the 'schedules' table in the database if it doesn't already exist.
        
        This function defines the 'schedules' table in the database and sets up the necessary fields,
        validations, labels, and widgets. If the 'schedules' table already exists, this function does nothing.
        
        Parameters:
        - self: The instance of the class.
        
        Returns:
        - None
        
        """
        if 'schedules' not in self.db.tables:
            self.db.define_table('schedules',
                            Field('block_start', 'time', required=True),
                            Field('block_end', 'time', required=True))

            # validation for 'schedules'
            self.db.schedules.block_start.requires = IS_NOT_EMPTY()
            self.db.schedules.block_end.requires = IS_NOT_EMPTY()

            # Etiquetas
            self.db.schedules.block_start.label = 'Hora Inicio'
            self.db.schedules.block_end.label = 'Hora Final'
            
            # Asignar widget de tiempo
            self.db.schedules.block_start.widget = TimeWidget.widget
            self.db.schedules.block_end.widget = TimeWidget.widget