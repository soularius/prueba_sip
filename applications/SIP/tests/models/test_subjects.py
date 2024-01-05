import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.subjects import Subjects

class TestSubjectsModel(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.db = DAL('sqlite:memory:')
        Subjects(self.db).define_table()
        current.db = self.db

    def test_validation(self):
        # Intentar crear un registro sin los campos requeridos
        try:
            self.db.subjects.insert()
            self.db.commit()
        except:
            self.db.rollback()

        # Comprobar que no se haya creado el registro
        self.assertEqual(self.db(self.db.subjects).count(), 0)

    def test_update_subject(self):
        # Actualizar una materia
        subject_id = self.db.subjects.insert(name="Matemáticas", description="Estudio de números y formas")
        self.db(self.db.subjects.id == subject_id).update(name="Física")
        updated_subject = self.db.subjects(subject_id)

        # Validar la actualización
        self.assertEqual(updated_subject.name, "Física")

    def test_delete_subject(self):
        # Eliminar una materia
        subject_id = self.db.subjects.insert(name="Matemáticas", description="Estudio de números y formas")
        self.db(self.db.subjects.id == subject_id).delete()
        deleted_subject = self.db.subjects(subject_id)

        # Validar la eliminación
        self.assertIsNone(deleted_subject)

    def tearDown(self):
        # Limpiar el entorno después de cada prueba
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
