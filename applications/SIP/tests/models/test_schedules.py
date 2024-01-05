import unittest
from gluon.dal import DAL
from gluon import current
import datetime

from applications.SIP.modules.models.schedules import Schedules

class TestSchedulesModel(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.db = DAL('sqlite:memory:')
        Schedules(self.db).define_table()
        current.db = self.db

    def test_create_schedule(self):
        # Crear un horario
        schedule_id = self.db.schedules.insert(block_start="08:00", block_end="10:00")

        # Recuperar el horario creado
        schedule_record = self.db.schedules(schedule_id)

        # Validar que el horario se haya creado correctamente
        self.assertIsNotNone(schedule_record)
        self.assertEqual(schedule_record.block_start, datetime.time(8, 0))
        self.assertEqual(schedule_record.block_end, datetime.time(10, 0))

    def test_validation(self):
        # Intentar crear un horario sin hora de inicio o final
        try:
            self.db.schedules.insert()
            self.db.commit()
        except:
            self.db.rollback()
        # Comprobar que no se haya creado el horario
        self.assertEqual(self.db(self.db.schedules).count(), 0)

    def test_update_schedule(self):
        # Actualizar un horario
        schedule_id = self.db.schedules.insert(block_start="08:00", block_end="10:00")
        self.db(self.db.schedules.id == schedule_id).update(block_start="09:00", block_end="11:00")
        updated_schedule = self.db.schedules(schedule_id)

        # Validar la actualización
        self.assertEqual(updated_schedule.block_start, datetime.time(9, 0))
        self.assertEqual(updated_schedule.block_end, datetime.time(11, 0))

    def test_delete_schedule(self):
        # Eliminar un horario
        schedule_id = self.db.schedules.insert(block_start="08:00", block_end="10:00")
        self.db(self.db.schedules.id == schedule_id).delete()
        deleted_schedule = self.db.schedules(schedule_id)

        # Validar la eliminación
        self.assertIsNone(deleted_schedule)

    def tearDown(self):
        # Limpiar el entorno después de cada prueba
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
