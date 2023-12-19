class SubjectsController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def grid(self):
        grid = self.SQLFORM.grid(self.db.subjects)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.subjects).process()
        if form.accepted:
            self.response.flash = 'Asignatura creado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, subject_id):
        salon = self.db.subjects(subject_id) or self.redirect(self.URL('error'))
        return dict(salon=salon)

    def update(self, subject_id):
        record = self.db.subjects(subject_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.subjects, record).process()
        if form.accepted:
            self.response.flash = 'Asignatura actualizada exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, subject_id):
        self.db(self.db.subjects.id == subject_id).delete()
        self.redirect(self.URL('list'))
