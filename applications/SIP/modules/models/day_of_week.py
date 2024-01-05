from gluon import *
from pydal.validators import ValidationError 
class DayOfWeek:    
    def __init__(self, db):
        self.db = db
    def define_table(self):
        """
        Defines the 'day_of_week' table in the database.

        This function checks if the 'day_of_week' table exists in the database. If it
        does not exist, it creates the table with the following fields:
        - 'name': a string field with a maximum length of 45 characters, unique and required.

        The 'name' field has the following validations:
        - It cannot be empty.
        - It must have a minimum length of 3 and a maximum length of 45.

        The 'name' field is labeled as 'Día de la semana' in the user interface.

        Parameters:
        - None

        Return:
        - None
        """
        if 'day_of_week' not in self.db.tables:
            self.db.define_table('day_of_week',
                            Field('name', 'string', length=45, unique=True, required=True))

            # validation for 'day_of_week'
            self.db.day_of_week.name.requires = [IS_NOT_EMPTY(), IS_LENGTH(maxsize=45, minsize= 3)]

            self.db.day_of_week.name.label = 'Día de la semana'    