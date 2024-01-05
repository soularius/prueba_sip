class TeachersController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        """
        Generates the index page for the application.

        :return: A dictionary containing the grid object.
        """
        grid = self.SQLFORM.grid(
            self.db.teachers,
            create=True,
            editable=True,
            deletable=True,
            details=True,
            user_signature=False
        )
        return dict(grid=grid)