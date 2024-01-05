var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { StudentController } from '../../controller/StudentController.js';
import { StudentRepository } from '../../repository/StudentRepository.js';
jest.mock('../../repository/StudentRepository');
// Describes test suite for StudentController
describe('StudentController', () => {
    let controller;
    let mockRepository;
    beforeEach(() => {
        // Initialize a mock repository and inject it into the controller before each test
        mockRepository = new StudentRepository();
        controller = new StudentController(mockRepository);
    });
    // Test to ensure listStudents method populates the container with the student list
    test('listStudents should populate the container with student list', () => __awaiter(void 0, void 0, void 0, function* () {
        // Mock data setup
        const mockStudents = [{ id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' }];
        mockRepository.listStudents.mockResolvedValue(mockStudents);
        const container = document.createElement('div');
        yield controller.listStudents(container, 1);
        // Assertions to verify container contents
        expect(container.innerHTML).toContain('Marta');
        expect(container.innerHTML).toContain('Salcedo');
        expect(container.innerHTML).toContain('123456789');
        expect(container.innerHTML).toContain('marta.salcedo@example.es');
    }));
    // Test to verify viewDetails method displays student details
    test('viewDetails should display student details', () => __awaiter(void 0, void 0, void 0, function* () {
        // Mock data setup
        const mockStudent = { id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' };
        mockRepository.getStudent.mockResolvedValue(mockStudent);
        const container = document.createElement('div');
        yield controller.viewDetails(container, 1);
        // Assertions to verify student information display
        expect(container.innerHTML).toContain('Marta');
        expect(container.innerHTML).toContain('Salcedo');
    }));
    // Test to ensure editStudent method displays an edit form for a student
    test('editStudent should display edit form for the student', () => __awaiter(void 0, void 0, void 0, function* () {
        // Mock data setup
        const mockStudent = { id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' };
        mockRepository.getStudent.mockResolvedValue(mockStudent);
        const container = document.createElement('div');
        yield controller.editStudent(container, 1);
        // Assertions to verify edit form display
        expect(container.innerHTML).toContain('Nombre');
        expect(container.innerHTML).toContain('Apellido');
        expect(container.innerHTML).toContain('Teléfono');
        expect(container.innerHTML).toContain('Correo Electrónico');
        expect(container.innerHTML).toContain('Actualizar Estudiante');
    }));
    // Test to verify deleteStudent method deletes a student
    test('deleteStudent should delete a student', () => __awaiter(void 0, void 0, void 0, function* () {
        // Mock user interactions and repository behavior
        window.alert = jest.fn();
        window.confirm = jest.fn().mockReturnValue(true);
        mockRepository.deleteStudent.mockResolvedValue();
        yield controller.deleteStudent(1);
        // Assertion to verify delete operation
        expect(mockRepository.deleteStudent).toHaveBeenCalledWith(1);
    }));
    // Test to ensure createStudent method displays a creation form
    test('createStudent should display create form', () => __awaiter(void 0, void 0, void 0, function* () {
        const container = document.createElement('div');
        yield controller.createStudent(container);
        // Assertions to verify creation form display
        expect(container.innerHTML).toContain('Nombre');
        expect(container.innerHTML).toContain('Apellido');
        expect(container.innerHTML).toContain('Teléfono');
        expect(container.innerHTML).toContain('Correo Electrónico');
        expect(container.innerHTML).toContain('Registrar Estudiante');
    }));
});
