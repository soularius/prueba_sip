var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { StudentRepository } from '../../repository/StudentRepository.js';
// Importa los mock que necesitas
describe('StudentRepository', () => {
    let studentRepository;
    beforeEach(() => {
        studentRepository = new StudentRepository();
        global.fetch = jest.fn();
    });
    test('getStudent retorna un estudiante cuando la solicitud es exitosa', () => __awaiter(void 0, void 0, void 0, function* () {
        const mockStudent = { id: 1, name: 'Juan' };
        global.fetch.mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ student: mockStudent, http_status: 200 })
        });
        const student = yield studentRepository.getStudent(1);
        expect(student).toEqual(mockStudent);
    }));
    test('getStudent retorna null si el estudiante no se encuentra', () => __awaiter(void 0, void 0, void 0, function* () {
        global.fetch.mockResolvedValue({
            ok: false,
            json: () => Promise.resolve({ status: 'error', message: 'Student not found' })
        });
        const student = yield studentRepository.getStudent(1);
        expect(student).toBeNull();
    }));
    test('listStudents retorna una lista de estudiantes cuando la solicitud es exitosa', () => __awaiter(void 0, void 0, void 0, function* () {
        const mockStudents = [{ id: 1, name: 'Juan' }, { id: 2, name: 'Ana' }];
        global.fetch.mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ students: mockStudents, http_status: 200 })
        });
        const students = yield studentRepository.listStudents(1);
        expect(students).toEqual(mockStudents);
    }));
    test('listStudents retorna null si hay un error', () => __awaiter(void 0, void 0, void 0, function* () {
        global.fetch.mockResolvedValue({
            ok: false,
            json: () => Promise.resolve({ message: 'Error' })
        });
        const students = yield studentRepository.listStudents(1);
        expect(students).toBeNull();
    }));
    test('createStudent llama a fetch con los parámetros correctos', () => __awaiter(void 0, void 0, void 0, function* () {
        // Asegúrate de que mockStudent tenga todas las propiedades requeridas
        const mockStudent = {
            name: 'Juan',
            lastname: 'Perez',
            phone: '1234567890',
            email: 'juan.perez@example.com'
        };
        global.fetch.mockResolvedValue({ ok: true });
        yield studentRepository.createStudent(mockStudent);
        expect(global.fetch).toHaveBeenCalledWith('/SIP/students/api_create_student', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mockStudent)
        });
    }));
    test('getTotalPages retorna el número total de páginas', () => __awaiter(void 0, void 0, void 0, function* () {
        global.fetch.mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ total_students: 50 })
        });
        const totalPages = yield studentRepository.getTotalPages(10);
        expect(totalPages).toBe(5);
    }));
    test('getStudent maneja errores de red', () => __awaiter(void 0, void 0, void 0, function* () {
        global.fetch.mockRejectedValue(new Error('Network error'));
        const student = yield studentRepository.getStudent(1);
        expect(student).toBeNull();
    }));
    test('updateStudent llama a fetch con los parámetros correctos', () => __awaiter(void 0, void 0, void 0, function* () {
        const mockStudent = { id: 1, name: 'Juan', lastname: 'Perez', phone: '1234567890', email: 'juan.perez@example.com' };
        const mockId = 1;
        global.fetch.mockResolvedValue({ ok: true });
        yield studentRepository.updateStudent(mockId, mockStudent);
        expect(global.fetch).toHaveBeenCalledWith(`/SIP/students/api_update_student/${mockId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mockStudent)
        });
    }));
    test('deleteStudent llama a fetch con los parámetros correctos', () => __awaiter(void 0, void 0, void 0, function* () {
        const mockId = 1;
        global.fetch.mockResolvedValue({ ok: true });
        yield studentRepository.deleteStudent(mockId);
        expect(global.fetch).toHaveBeenCalledWith(`/SIP/students/api_delete_student/${mockId}`, {
            method: 'DELETE'
        });
    }));
    test('Maneja errores al obtener un estudiante', () => __awaiter(void 0, void 0, void 0, function* () {
        // Configurar el mock de fetch para simular un error
        global.fetch.mockRejectedValue(new Error('Error al obtener el estudiante'));
        // Crear un spy en console.error antes de ejecutar la función que genera el error
        const consoleSpy = jest.spyOn(console, 'error');
        // Intentar obtener un estudiante para desencadenar el error
        yield studentRepository.getStudent(1);
        // Verificar si se llamó a console.error con el mensaje correcto
        expect(consoleSpy).toHaveBeenCalledWith('Error al obtener el estudiante:', expect.any(Error));
        // Restaurar el comportamiento original de console.error
        consoleSpy.mockRestore();
    }));
});
