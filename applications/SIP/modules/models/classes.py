from gluon import *
from gluon.sqlhtml import OptionsWidget

class Classes:
    def __init__(self, db):
        self.db = db
    def define_table(self):
        if 'classes' not in self.db.tables:
            self.db.define_table('classes',
                            Field('code', 'string', length=55, unique=True),
                            Field('salon_id', 'reference salons', ondelete='CASCADE'),
                            Field('subject_id', 'reference subjects', ondelete='CASCADE'),
                            Field('schedule_id', 'reference schedules', ondelete='CASCADE'),
                            Field('teacher_id', 'reference teachers', ondelete='CASCADE'),
                            Field('day_of_week_id', 'reference day_of_week', ondelete='CASCADE'))
            
            # Validation for 'classes'
            self.db.classes.salon_id.requires = [IS_IN_DB(self.db, self.db.salons.id, '%(name)s')]
            self.db.classes.subject_id.requires = [IS_IN_DB(self.db, self.db.subjects.id, '%(name)s')]
            self.db.classes.schedule_id.requires = [IS_IN_DB(self.db, self.db.schedules.id, '%(block_start)s - %(block_end)s')]
            self.db.classes.teacher_id.requires = [IS_IN_DB(self.db, self.db.teachers.id, '%(name)s %(lastname)s')]
            self.db.classes.day_of_week_id.requires = [IS_IN_DB(self.db, self.db.day_of_week.id, '%(name)s')]

            self.db.classes.salon_id.represent = lambda value, row: self.db.salons(value).name
            self.db.classes.subject_id.represent = lambda value, row: self.db.subjects(value).name
            self.db.classes.schedule_id.represent = lambda value, row: f"{self.db.schedules(value).block_start} - {self.db.schedules(value).block_end}"
            self.db.classes.teacher_id.represent = lambda value, row: f"{self.db.teachers(value).name} {self.db.teachers(value).lastname}"
            self.db.classes.day_of_week_id.represent = lambda value, row: self.db.day_of_week(value).name

            self.db.classes.salon_id.widget = OptionsWidget.widget
            self.db.classes.subject_id.widget = OptionsWidget.widget
            self.db.classes.schedule_id.widget = OptionsWidget.widget
            self.db.classes.teacher_id.widget = OptionsWidget.widget
            self.db.classes.day_of_week_id.widget = OptionsWidget.widget

            self.db.classes.code.label = 'Código de la Clase'
            self.db.classes.salon_id.label = 'Salón'
            self.db.classes.subject_id.label = 'Materia'
            self.db.classes.schedule_id.label = 'Horario'
            self.db.classes.teacher_id.label = 'Profesor/a'
            self.db.classes.day_of_week_id.label = 'Día de la Semana'