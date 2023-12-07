def manage_teachers():
    grid = SQLFORM.grid(db.teachers)
    return dict(grid=grid)