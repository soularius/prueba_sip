class SubjectsController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        """
        Return a dictionary containing a grid object for the subjects table.
        """
        grid = self.SQLFORM.grid(
            self.db.subjects,
            create=True,
            editable=True,
            deletable=True,
            details=True,
            user_signature=False
        )
        return dict(grid=grid)