import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.day_of_week import DayOfWeek

class TestDayOfWeekModel(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.db = DAL('sqlite:memory:')
        DayOfWeek(self.db).define_table()
        current.db = self.db

    def test_create_day_of_week(self):
        # Crear un registro en 'day_of_week'
        day_id = self.db.day_of_week.insert(name="Lunes")

        # Recuperar el registro creado
        day_record = self.db.day_of_week(day_id)

        # Validar que el registro se haya creado correctamente
        self.assertIsNotNone(day_record)
        self.assertEqual(day_record.name, "Lunes")

    def test_validation(self):
        # Intentar crear un registro sin nombre
        try:
            self.db.day_of_week.insert()
            self.db.commit()
        except:
            self.db.rollback()
        # Comprobar que no se haya creado el registro
        self.assertEqual(self.db(self.db.day_of_week).count(), 0)

    def test_label(self):
        # Comprobar la etiqueta del campo 'name'
        self.assertEqual(self.db.day_of_week.name.label, 'Día de la semana')

    def tearDown(self):
        # Limpiar el entorno después de cada prueba
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
