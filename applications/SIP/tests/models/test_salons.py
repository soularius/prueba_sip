import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.salons import Salons

class TestSalonsModel(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.db = DAL('sqlite:memory:')
        Salons(self.db).define_table()
        current.db = self.db

    def test_create_salon(self):
        # Crear un registro en 'salons'
        salon_id = self.db.salons.insert(name="Salón 101", description="Salón de clases principal")

        # Recuperar el registro creado
        salon_record = self.db.salons(salon_id)

        # Validar que el registro se haya creado correctamente
        self.assertIsNotNone(salon_record)
        self.assertEqual(salon_record.name, "Salón 101")
        self.assertEqual(salon_record.description, "Salón de clases principal")

    def test_validation(self):
        # Intentar crear un registro sin nombre o descripción
        try:
            self.db.salons.insert()
            self.db.commit()
        except:
            self.db.rollback()

        # Comprobar que no se haya creado el registro
        self.assertEqual(self.db(self.db.salons).count(), 0)

    def test_update_salon(self):
        # Actualizar un salón
        salon_id = self.db.salons.insert(name="Salón 101", description="Salón de clases principal")
        self.db(self.db.salons.id == salon_id).update(name="Salón 102")
        updated_salon = self.db.salons(salon_id)

        # Validar la actualización
        self.assertEqual(updated_salon.name, "Salón 102")

    def test_delete_salon(self):
        # Eliminar un salón
        salon_id = self.db.salons.insert(name="Salón 101", description="Salón de clases principal")
        self.db(self.db.salons.id == salon_id).delete()
        deleted_salon = self.db.salons(salon_id)

        # Validar la eliminación
        self.assertIsNone(deleted_salon)

    def tearDown(self):
        # Limpiar el entorno después de cada prueba
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
