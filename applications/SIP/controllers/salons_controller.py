class SalonsController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        """
        Generate the index page.

        Returns:
            dict: A dictionary containing the grid object.
        """
        grid = self.SQLFORM.grid(
            self.db.salons,
            create=True,
            editable=True,
            deletable=True,
            details=True,
            user_signature=False
        )
        return dict(grid=grid)