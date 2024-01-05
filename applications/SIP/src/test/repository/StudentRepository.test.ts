import { StudentRepository } from '../../repository/StudentRepository';
// Importa los mock que necesitas

describe('StudentRepository', () => {
    let studentRepository: StudentRepository;

    beforeEach(() => {
        studentRepository = new StudentRepository();
        global.fetch = jest.fn();
        global.alert = jest.fn();
    });

    test('getStudent retorna un estudiante cuando la solicitud es exitosa', async () => {
        const mockStudent = { id: 1, name: 'Juan' };
        (global.fetch as jest.Mock).mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ student: mockStudent, http_status: 200 })
        });

        const student = await studentRepository.getStudent(1);
        expect(student).toEqual(mockStudent);
    });

    test('getStudent retorna null si el estudiante no se encuentra', async () => {
        (global.fetch as jest.Mock).mockResolvedValue({
            ok: false,
            json: () => Promise.resolve({ status: 'error', message: 'Student not found' })
        });

        const student = await studentRepository.getStudent(1);
        expect(student).toBeNull();
    });

    test('listStudents retorna una lista de estudiantes cuando la solicitud es exitosa', async () => {
        const mockStudents = [{ id: 1, name: 'Juan' }, { id: 2, name: 'Ana' }];
        (global.fetch as jest.Mock).mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ students: mockStudents, http_status: 200 })
        });
    
        const students = await studentRepository.listStudents(1);
        expect(students).toEqual(mockStudents);
    });
    
    test('listStudents retorna null si hay un error', async () => {
        (global.fetch as jest.Mock).mockResolvedValue({
            ok: false,
            json: () => Promise.resolve({ message: 'Error' })
        });
    
        const students = await studentRepository.listStudents(1);
        expect(students).toBeNull();
    });

    test('createStudent llama a fetch con los parámetros correctos', async () => {
        // Asegúrate de que mockStudent tenga todas las propiedades requeridas
        const mockStudent = {
            name: 'Juan',
            lastname: 'Perez',
            phone: '1234567890',
            email: 'juan.perez@example.com'
        };
    
        (global.fetch as jest.Mock).mockResolvedValue({ ok: true });
    
        await studentRepository.createStudent(mockStudent);
        expect(global.fetch).toHaveBeenCalledWith('/SIP/students/api_create_student', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(mockStudent)
        });
    });

    test('getTotalPages retorna el número total de páginas', async () => {
        (global.fetch as jest.Mock).mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ total_students: 50 })
        });
    
        const totalPages = await studentRepository.getTotalPages(10);
        expect(totalPages).toBe(5);
    });

    test('getStudent maneja errores de red', async () => {
        (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));
    
        const student = await studentRepository.getStudent(1);
        expect(student).toBeNull();
    });

    test('listStudents maneja errores de red', async () => {
        (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));
    
        const students = await studentRepository.listStudents(1);
        expect(students).toBeNull();
    });
    
    test('updateStudent llama a fetch con los parámetros correctos', async () => {
        const mockStudent = { id: 1, name: 'Juan', lastname: 'Perez', phone: '1234567890', email: 'juan.perez@example.com' };
        const mockId = 1;
        (global.fetch as jest.Mock).mockResolvedValue({ ok: true });
    
        await studentRepository.updateStudent(mockId, mockStudent);
        expect(global.fetch).toHaveBeenCalledWith(`/SIP/students/api_update_student/${mockId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(mockStudent)
        });
    });
    
    test('deleteStudent llama a fetch con los parámetros correctos', async () => {
        const mockId = 1;
        (global.fetch as jest.Mock).mockResolvedValue({ ok: true });
    
        await studentRepository.deleteStudent(mockId);
        expect(global.fetch).toHaveBeenCalledWith(`/SIP/students/api_delete_student/${mockId}`, {
            method: 'DELETE'
        });
    });
    
    test('Maneja errores al obtener un estudiante', async () => {
        // Configurar el mock de fetch para simular un error
        (global.fetch as jest.Mock).mockRejectedValue(new Error('Error al obtener el estudiante'));

        // Crear un spy en alert antes de ejecutar la función que genera el error
        const alertSpy = jest.spyOn(window, 'alert');
    
        // Intentar obtener un estudiante para desencadenar el error
        await studentRepository.getStudent(1);
    
        // Verificar si se llamó a alert con el mensaje correcto
        expect(alertSpy).toHaveBeenCalledWith('Error al obtener el estudiante: Error: Error al obtener el estudiante');
    
        // Restaurar el comportamiento original de alert
        alertSpy.mockRestore();
    });
});
