class ClassesStudentsController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM

    def index(self):
        grid = self.SQLFORM.grid(self.db.classes_students)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.classes_students).process()
        if form.accepted:
            self.response.flash = 'Clase estudio creada exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, classes_students_id):
        classes_students = self.db.classes_students(classes_students_id) or self.redirect(self.URL('error'))
        return dict(classes_students=classes_students)

    def update(self, classes_students_id):
        record = self.db.classes_students(classes_students_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.classes_students, record).process()
        if form.accepted:
            self.response.flash = 'Clase estudio actualizada exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, classes_students_id):
        self.db(self.db.classes_students.id == classes_students_id).delete()
        self.redirect(self.URL('list'))
