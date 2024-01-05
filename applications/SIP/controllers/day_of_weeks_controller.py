class DayOfWeeksController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        """
        This function returns a dictionary containing a SQLFORM.grid object assigned to the 'grid' key.

        :return: A dictionary with the 'grid' key assigned to a SQLFORM.grid object.
        """
        grid = self.SQLFORM.grid(
            self.db.day_of_week,
            create=True,
            editable=True,
            deletable=True,
            details=True,
            user_signature=False
        )
        return dict(grid=grid)