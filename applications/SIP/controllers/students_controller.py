class StudentsController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        """
        A function that returns a dictionary containing a grid object.

        :param self: The current instance of the class.
        :return: A dictionary with the 'grid' key that contains the grid object.
        """
        grid = self.SQLFORM.grid(
            self.db.students,
            create=True,
            editable=True,
            deletable=True,
            details=True,
            user_signature=False
        )
        return dict(grid=grid)