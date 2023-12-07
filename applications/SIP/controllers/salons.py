# Controlador para gestionar salones
def manage_salons():
    grid = SQLFORM.grid(db.salons)
    return locals()
