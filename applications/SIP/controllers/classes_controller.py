class ClassesController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        grid = self.SQLFORM.grid(self.db.classes)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.classes).process()
        if form.accepted:
            self.response.flash = 'Clase creada exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, classe_id):
        classe = self.db.classes(classe_id) or self.redirect(self.URL('error'))
        return dict(classe=classe)

    def update(self, classe_id):
        record = self.db.classes(classe_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.classes, record).process()
        if form.accepted:
            self.response.flash = 'Clase actualizada exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, classe_id):
        self.db(self.db.classes.id == classe_id).delete()
        self.redirect(self.URL('list'))
