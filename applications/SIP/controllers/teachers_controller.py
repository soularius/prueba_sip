class TeachersController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        grid = self.SQLFORM.grid(self.db.teachers)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.teachers).process()
        if form.accepted:
            self.response.flash = 'Profesor creado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, teacher_id):
        salon = self.db.teachers(teacher_id) or self.redirect(self.URL('error'))
        return dict(salon=salon)

    def update(self, teacher_id):
        record = self.db.teachers(teacher_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.teachers, record).process()
        if form.accepted:
            self.response.flash = 'Profesor actualizada exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, teacher_id):
        self.db(self.db.teachers.id == teacher_id).delete()
        self.redirect(self.URL('list'))
