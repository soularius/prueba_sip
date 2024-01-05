class ClassesController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        """
        Retrieves all the records from the "classes" table and displays them in a grid.
        
        :param self: The instance of the current class.
        :return: A dictionary containing the "grid" object.
        """
        grid = self.SQLFORM.grid(
            self.db.classes,
            create=True,
            editable=True,
            deletable=True,
            details=True,
            user_signature=False
        )
        return dict(grid=grid)