import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.classes import Classes
from applications.SIP.modules.models.salons import Salons
from applications.SIP.modules.models.subjects import Subjects
from applications.SIP.modules.models.schedules import Schedules
from applications.SIP.modules.models.teachers import Teachers
from applications.SIP.modules.models.day_of_week import DayOfWeek

class TestClassesModel(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.db = DAL('sqlite:memory:')
        Salons(self.db).define_table()
        Subjects(self.db).define_table()
        Schedules(self.db).define_table()
        Teachers(self.db).define_table()
        DayOfWeek(self.db).define_table()
        Classes(self.db).define_table()
        current.db = self.db

    def test_create_class(self):
        # Crear registros para las tablas referenciadas
        salon_id = self.db.salons.insert(name="Salon 1", description="Salón 1")
        subject_id = self.db.subjects.insert(name="Matemáticas", description="Matemáticas")
        schedule_id = self.db.schedules.insert(block_start='08:00:00', block_end='10:00:00')
        teacher_id = self.db.teachers.insert(name="Juan", lastname="Pérez", email="juan@example.com", phone="123456789")
        day_of_week_id = self.db.day_of_week.insert(name="Lunes")

        # Crear un registro en la tabla 'classes'
        class_id = self.db.classes.insert(
            code="CL01",
            salon_id=salon_id,
            subject_id=subject_id,
            schedule_id=schedule_id,
            teacher_id=teacher_id,
            day_of_week_id=day_of_week_id
        )

        # Recuperar el registro creado
        class_record = self.db.classes(class_id)

        # Validar que el registro se haya creado correctamente
        self.assertIsNotNone(class_record)
        self.assertEqual(class_record.code, "CL01")

    def test_field_representations(self):
        # Crear registros para las tablas referenciadas
        salon_id = self.db.salons.insert(name="Salon 2", description="Salón 2")
        subject_id = self.db.subjects.insert(name="Física", description="Física")
        schedule_id = self.db.schedules.insert(block_start='10:00:00', block_end='12:00:00')
        teacher_id = self.db.teachers.insert(name="Ana", lastname="López", email="anaa@example.com", phone="12346789")
        day_of_week_id = self.db.day_of_week.insert(name="Martes")

        # Crear un registro en 'classes'
        class_id = self.db.classes.insert(
            code="CL02",
            salon_id=salon_id,
            subject_id=subject_id,
            schedule_id=schedule_id,
            teacher_id=teacher_id,
            day_of_week_id=day_of_week_id
        )

        # Recuperar el registro creado
        class_record = self.db.classes(class_id)

        # Probar las representaciones de campo
        self.assertEqual(self.db.classes.salon_id.represent(class_record.salon_id, class_record), "Salon 2")
        self.assertEqual(self.db.classes.subject_id.represent(class_record.subject_id, class_record), "Física")
        self.assertEqual(self.db.classes.schedule_id.represent(class_record.schedule_id, class_record), "10:00:00 - 12:00:00")
        self.assertEqual(self.db.classes.teacher_id.represent(class_record.teacher_id, class_record), "Ana López")
        self.assertEqual(self.db.classes.day_of_week_id.represent(class_record.day_of_week_id, class_record), "Martes")

    def tearDown(self):
        # Limpiar el entorno después de cada prueba
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
