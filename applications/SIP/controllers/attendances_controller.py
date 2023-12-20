class AttendancesController:
    def __init__(self, db, SQLFORM):
        self.db = db
        self.SQLFORM = SQLFORM
    
    def index(self):
        grid = self.SQLFORM.grid(self.db.attendance)
        return dict(grid=grid)

    def create(self):
        form = self.SQLFORM(self.db.attendance).process()
        if form.accepted:
            self.response.flash = 'Asistencia creada exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def read(self, attendance_id):
        attendance = self.db.attendance(attendance_id) or self.redirect(self.URL('error'))
        return dict(attendance=attendance)

    def update(self, attendance_id):
        record = self.db.attendance(attendance_id) or self.redirect(self.URL('error'))
        form = self.SQLFORM(self.db.attendance, record).process()
        if form.accepted:
            self.response.flash = 'Asistencia actualizada exitosamente'
        elif form.errors:
            self.response.flash = 'El formulario tiene errores'
        return dict(form=form)

    def delete(self, attendance_id):
        self.db(self.db.attendance.id == attendance_id).delete()
        self.redirect(self.URL('list'))
