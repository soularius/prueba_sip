import { StudentController } from '../../controller/StudentController';
import { StudentRepository } from '../../repository/StudentRepository';
import { Student } from '../../models/Student';

jest.mock('../../repository/StudentRepository');

// Describes test suite for StudentController
describe('StudentController', () => {
  let controller: StudentController;
  let mockRepository: jest.Mocked<StudentRepository>;

  beforeEach(() => {
    // Initialize a mock repository and inject it into the controller before each test
    mockRepository = new StudentRepository() as jest.Mocked<StudentRepository>;
    controller = new StudentController(mockRepository);
  });

  // Test to ensure listStudents method populates the container with the student list
  test('listStudents should populate the container with student list', async () => {
    // Mock data setup
    const mockStudents: Student[] = [{ id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' }];
    mockRepository.listStudents.mockResolvedValue(mockStudents);
  
    const container = document.createElement('div');
    await controller.listStudents(container, 1);
  
    // Assertions to verify container contents
    expect(container.innerHTML).toContain('Marta');
    expect(container.innerHTML).toContain('Salcedo');
    expect(container.innerHTML).toContain('123456789');
    expect(container.innerHTML).toContain('marta.salcedo@example.es');
  });

  // Test to verify viewDetails method displays student details
  test('viewDetails should display student details', async () => {
    // Mock data setup
    const mockStudent: Student = { id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' };
    mockRepository.getStudent.mockResolvedValue(mockStudent);
  
    const container = document.createElement('div');
    await controller.viewDetails(container, 1);
  
    // Assertions to verify student information display
    expect(container.innerHTML).toContain('Marta');
    expect(container.innerHTML).toContain('Salcedo');
  });

  // Test to ensure editStudent method displays an edit form for a student
  test('editStudent should display edit form for the student', async () => {
    // Mock data setup
    const mockStudent: Student = { id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' };
    mockRepository.getStudent.mockResolvedValue(mockStudent);
  
    const container = document.createElement('div');
    await controller.editStudent(container, 1);
  
    // Assertions to verify edit form display
    expect(container.innerHTML).toContain('Nombre');
    expect(container.innerHTML).toContain('Apellido');
    expect(container.innerHTML).toContain('Teléfono');
    expect(container.innerHTML).toContain('Correo Electrónico');
    expect(container.innerHTML).toContain('Actualizar Estudiante');
  });

  // Test to verify deleteStudent method deletes a student
  test('deleteStudent should delete a student', async () => {
    // Mock user interactions and repository behavior
    window.alert = jest.fn();
    window.confirm = jest.fn().mockReturnValue(true);
    mockRepository.deleteStudent.mockResolvedValue();
  
    await controller.deleteStudent(1);
  
    // Assertion to verify delete operation
    expect(mockRepository.deleteStudent).toHaveBeenCalledWith(1);
  });

  // Test to ensure createStudent method displays a creation form
  test('createStudent should display create form', async () => {
    const container = document.createElement('div');
    await controller.createStudent(container);
  
    // Assertions to verify creation form display
    expect(container.innerHTML).toContain('Nombre');
    expect(container.innerHTML).toContain('Apellido');
    expect(container.innerHTML).toContain('Teléfono');
    expect(container.innerHTML).toContain('Correo Electrónico');
    expect(container.innerHTML).toContain('Registrar Estudiante');
  });
});