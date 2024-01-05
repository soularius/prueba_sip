import { StudentController } from '../../controller/StudentController';
import { StudentRepository } from '../../repository/StudentRepository';
import { Student } from '../../models/Student';

jest.mock('../../repository/StudentRepository');

describe('StudentController', () => {
  let controller: StudentController;
  let mockRepository: jest.Mocked<StudentRepository>;

  beforeEach(() => {
    // Crear un mock del repositorio
    mockRepository = new StudentRepository() as jest.Mocked<StudentRepository>;
    // Inyectar el mock del repositorio en el controlador
    controller = new StudentController(mockRepository);
  });

  test('listStudents should populate the container with student list', async () => {
    const mockStudents: Student[] = [{ id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' }];
    // Configurar el comportamiento del mock
    mockRepository.listStudents.mockResolvedValue(mockStudents);
  
    const container = document.createElement('div');
    await controller.listStudents(container, 1);
  
    // Afirmaciones sobre el contenido del contenedor
    expect(container.innerHTML).toContain('Marta');
    expect(container.innerHTML).toContain('Salcedo');
    expect(container.innerHTML).toContain('123456789');
    expect(container.innerHTML).toContain('marta.salcedo@example.es');
  });

  test('viewDetails should display student details', async () => {
    const mockStudent: Student = { id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' };
    mockRepository.getStudent.mockResolvedValue(mockStudent);
  
    const container = document.createElement('div');
    await controller.viewDetails(container, 1);
  
    // Verificar que se muestra la información del estudiante
    expect(container.innerHTML).toContain('Marta');
    expect(container.innerHTML).toContain('Salcedo');
  });
  
  test('editStudent should display edit form for the student', async () => {
    const mockStudent: Student = { id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' };
    mockRepository.getStudent.mockResolvedValue(mockStudent);
  
    const container = document.createElement('div');
    await controller.editStudent(container, 1);
  
    // Verificar que se muestra el formulario de edición
    expect(container.innerHTML).toContain('Nombre');
    expect(container.innerHTML).toContain('Apellido');
    expect(container.innerHTML).toContain('Teléfono');
    expect(container.innerHTML).toContain('Correo Electrónico');
    expect(container.innerHTML).toContain('Actualizar Estudiante'); // Texto corregido
  });
 

  test('deleteStudent should delete a student', async () => {
    window.alert = jest.fn();
    window.confirm = jest.fn().mockReturnValue(true);
    mockRepository.deleteStudent.mockResolvedValue();
  
    // Llamada al método deleteStudent
    await controller.deleteStudent(1);
  
    // Verificar que se llamó al método deleteStudent del repositorio
    expect(mockRepository.deleteStudent).toHaveBeenCalledWith(1);
  });

  test('createStudent should display create form', async () => {
    const container = document.createElement('div');
    await controller.createStudent(container);
  
    // Verificar que se muestra el formulario de creación
    expect(container.innerHTML).toContain('Nombre');
    expect(container.innerHTML).toContain('Apellido');
    expect(container.innerHTML).toContain('Teléfono');
    expect(container.innerHTML).toContain('Correo Electrónico');
    expect(container.innerHTML).toContain('Registrar Estudiante');
  });
  
});
