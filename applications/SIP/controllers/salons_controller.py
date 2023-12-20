class SalonsController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        grid = self.SQLFORM.grid(self.db.salons)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.salons).process()
        if form.accepted:
            self.response.flash = 'Salón creado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, salon_id):
        salon = self.db.salons(salon_id) or self.redirect(self.URL('error'))
        return dict(salon=salon)

    def update(self, salon_id):
        record = self.db.salons(salon_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.salons, record).process()
        if form.accepted:
            self.response.flash = 'Salón actualizado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, salon_id):
        self.db(self.db.salons.id == salon_id).delete()
        self.redirect(self.URL('list'))
