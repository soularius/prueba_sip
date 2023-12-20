class DayOfWeeksController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        grid = self.SQLFORM.grid(self.db.day_of_week)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.day_of_week).process()
        if form.accepted:
            self.response.flash = 'Dia de la semana creado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, day_of_week_id):
        salon = self.db.day_of_week(day_of_week_id) or self.redirect(self.URL('error'))
        return dict(salon=salon)

    def update(self, day_of_week_id):
        record = self.db.day_of_week(day_of_week_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.day_of_week, record).process()
        if form.accepted:
            self.response.flash = 'Dia de la semana actualizado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, day_of_week_id):
        self.db(self.db.day_of_week.id == day_of_week_id).delete()
        self.redirect(self.URL('list'))
