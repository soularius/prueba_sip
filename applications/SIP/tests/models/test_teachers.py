import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.teachers import Teachers

class TestTeachersModel(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.db = DAL('sqlite:memory:')
        Teachers(self.db).define_table()
        current.db = self.db

    def test_validation(self):
        # Intentar crear un registro sin los campos requeridos
        try:
            self.db.teachers.insert()
            self.db.commit()
        except:
            self.db.rollback()

        # Comprobar que no se haya creado el registro
        self.assertEqual(self.db(self.db.teachers).count(), 0)

    def test_update_teacher(self):
        # Actualizar un profesor
        teacher_id = self.db.teachers.insert(name="Juan", lastname="Pérez", email="juan@example.com", phone="1234567890")
        self.db(self.db.teachers.id == teacher_id).update(name="Carlos")
        updated_teacher = self.db.teachers(teacher_id)

        # Validar la actualización
        self.assertEqual(updated_teacher.name, "Carlos")

    def test_delete_teacher(self):
        # Eliminar un profesor
        teacher_id = self.db.teachers.insert(name="Juan", lastname="Pérez", email="juan@example.com", phone="1234567890")
        self.db(self.db.teachers.id == teacher_id).delete()
        deleted_teacher = self.db.teachers(teacher_id)

        # Validar la eliminación
        self.assertIsNone(deleted_teacher)

    def tearDown(self):
        # Limpiar el entorno después de cada prueba
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
