class StudentsController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        grid = self.SQLFORM.grid(self.db.students)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.students).process()
        if form.accepted:
            self.response.flash = 'Estudiante creado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, students_id):
        student = self.db.students(students_id) or self.redirect(self.URL('error'))
        return dict(student=student)

    def update(self, students_id):
        record = self.db.students(students_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.students, record).process()
        if form.accepted:
            self.response.flash = 'Estudiante actualizado exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, students_id):
        self.db(self.db.students.id == students_id).delete()
        self.redirect(self.URL('list'))
