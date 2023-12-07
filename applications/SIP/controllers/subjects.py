def manage_subjects():
    grid = SQLFORM.grid(db.subjects)
    return dict(grid=grid)