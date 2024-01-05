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
describe('StudentController', () => {
    let controller;
    let mockRepository;
    beforeEach(() => {
        // Crear un mock del repositorio
        mockRepository = new StudentRepository();
        // Inyectar el mock del repositorio en el controlador
        controller = new StudentController(mockRepository);
    });
    test('listStudents should populate the container with student list', () => __awaiter(void 0, void 0, void 0, function* () {
        const mockStudents = [{ id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' }];
        // Configurar el comportamiento del mock
        mockRepository.listStudents.mockResolvedValue(mockStudents);
        const container = document.createElement('div');
        yield controller.listStudents(container, 1);
        // Afirmaciones sobre el contenido del contenedor
        expect(container.innerHTML).toContain('Marta');
        expect(container.innerHTML).toContain('Salcedo');
        expect(container.innerHTML).toContain('123456789');
        expect(container.innerHTML).toContain('marta.salcedo@example.es');
    }));
    test('viewDetails should display student details', () => __awaiter(void 0, void 0, void 0, function* () {
        const mockStudent = { id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' };
        mockRepository.getStudent.mockResolvedValue(mockStudent);
        const container = document.createElement('div');
        yield controller.viewDetails(container, 1);
        // Verificar que se muestra la información del estudiante
        expect(container.innerHTML).toContain('Marta');
        expect(container.innerHTML).toContain('Salcedo');
    }));
    test('editStudent should display edit form for the student', () => __awaiter(void 0, void 0, void 0, function* () {
        const mockStudent = { id: 1, name: 'Marta', lastname: 'Salcedo', email: 'marta.salcedo@example.es', phone: '123456789' };
        mockRepository.getStudent.mockResolvedValue(mockStudent);
        const container = document.createElement('div');
        yield controller.editStudent(container, 1);
        // Verificar que se muestra el formulario de edición
        expect(container.innerHTML).toContain('Nombre');
        expect(container.innerHTML).toContain('Apellido');
        expect(container.innerHTML).toContain('Teléfono');
        expect(container.innerHTML).toContain('Correo Electrónico');
        expect(container.innerHTML).toContain('Actualizar Estudiante'); // Texto corregido
    }));
    test('deleteStudent should delete a student', () => __awaiter(void 0, void 0, void 0, function* () {
        window.alert = jest.fn();
        window.confirm = jest.fn().mockReturnValue(true);
        mockRepository.deleteStudent.mockResolvedValue();
        // Llamada al método deleteStudent
        yield controller.deleteStudent(1);
        // Verificar que se llamó al método deleteStudent del repositorio
        expect(mockRepository.deleteStudent).toHaveBeenCalledWith(1);
    }));
    test('createStudent should display create form', () => __awaiter(void 0, void 0, void 0, function* () {
        const container = document.createElement('div');
        yield controller.createStudent(container);
        // Verificar que se muestra el formulario de creación
        expect(container.innerHTML).toContain('Nombre');
        expect(container.innerHTML).toContain('Apellido');
        expect(container.innerHTML).toContain('Teléfono');
        expect(container.innerHTML).toContain('Correo Electrónico');
        expect(container.innerHTML).toContain('Registrar Estudiante');
    }));
});
