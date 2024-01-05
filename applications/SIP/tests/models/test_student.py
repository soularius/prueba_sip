import unittest
from gluon.dal import DAL
from gluon import current

from applications.SIP.modules.models.student import Student

class TestStudentModel(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.db = DAL('sqlite:memory:')
        Student(self.db).define_table()
        current.db = self.db

    def test_validation(self):
        # Intentar crear un registro sin los campos requeridos
        try:
            self.db.students.insert()
            self.db.commit()
        except:
            self.db.rollback()

        # Comprobar que no se haya creado el registro
        self.assertEqual(self.db(self.db.students).count(), 0)

    def test_update_student(self):
        # Actualizar un estudiante
        student_id = self.db.students.insert(name="John", lastname="Doe", phone="1234567890", email="john@example.com")
        self.db(self.db.students.id == student_id).update(name="Jane")
        updated_student = self.db.students(student_id)

        # Validar la actualización
        self.assertEqual(updated_student.name, "Jane")

    def test_delete_student(self):
        # Eliminar un estudiante
        student_id = self.db.students.insert(name="John", lastname="Doe", phone="1234567890", email="john@example.com")
        self.db(self.db.students.id == student_id).delete()
        deleted_student = self.db.students(student_id)

        # Validar la eliminación
        self.assertIsNone(deleted_student)

    def tearDown(self):
        # Limpiar el entorno después de cada prueba
        self.db.close()
        current.db = None

if __name__ == '__main__':
    unittest.main()
