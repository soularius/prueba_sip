class SchedulesController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        grid = self.SQLFORM.grid(self.db.schedules)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.schedules).process()
        if form.accepted:
            self.response.flash = 'Horario creado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, schedule_id):
        schedule = self.db.schedules(schedule_id) or self.redirect(self.URL('error'))
        return dict(schedule=schedule)

    def update(self, schedule_id):
        record = self.db.schedules(schedule_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.schedules, record).process()
        if form.accepted:
            self.response.flash = 'Horario actualizado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, schedule_id):
        self.db(self.db.schedules.id == schedule_id).delete()
        self.redirect(self.URL('list'))
