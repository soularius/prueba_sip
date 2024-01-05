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
// Import necessary mocks
// Describes test suite for StudentRepository
describe('StudentRepository', () => {
    let studentRepository;
    beforeEach(() => {
        // Initialize StudentRepository and mock global functions before each test
        studentRepository = new StudentRepository();
        global.fetch = jest.fn();
        global.alert = jest.fn();
    });
    // Test to verify successful retrieval of a student
    test('getStudent returns a student when the request is successful', () => __awaiter(void 0, void 0, void 0, function* () {
        // Define mock student data and setup fetch mock
        const mockStudent = { id: 1, name: 'Juan' };
        global.fetch.mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ student: mockStudent, http_status: 200 })
        });
        // Call getStudent and assert the result
        const student = yield studentRepository.getStudent(1);
        expect(student).toEqual(mockStudent);
    }));
    // Test to verify handling of non-existent student
    test('getStudent returns null if the student is not found', () => __awaiter(void 0, void 0, void 0, function* () {
        // Setup fetch mock for failure response
        global.fetch.mockResolvedValue({
            ok: false,
            json: () => Promise.resolve({ status: 'error', message: 'Student not found' })
        });
        // Call getStudent and assert the result
        const student = yield studentRepository.getStudent(1);
        expect(student).toBeNull();
    }));
    // Test to verify successful retrieval of a list of students
    test('listStudents returns a list of students when the request is successful', () => __awaiter(void 0, void 0, void 0, function* () {
        // Define mock students data and setup fetch mock
        const mockStudents = [{ id: 1, name: 'Juan' }, { id: 2, name: 'Ana' }];
        global.fetch.mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ students: mockStudents, http_status: 200 })
        });
        // Call listStudents and assert the result
        const students = yield studentRepository.listStudents(1);
        expect(students).toEqual(mockStudents);
    }));
    // Test to verify handling of error in student list retrieval
    test('listStudents returns null if there is an error', () => __awaiter(void 0, void 0, void 0, function* () {
        // Setup fetch mock for failure response
        global.fetch.mockResolvedValue({
            ok: false,
            json: () => Promise.resolve({ message: 'Error' })
        });
        // Call listStudents and assert the result
        const students = yield studentRepository.listStudents(1);
        expect(students).toBeNull();
    }));
    // Test to verify correct API call for creating a student
    test('createStudent calls fetch with the correct parameters', () => __awaiter(void 0, void 0, void 0, function* () {
        // Define mock student data
        const mockStudent = {
            name: 'Juan',
            lastname: 'Perez',
            phone: '1234567890',
            email: 'juan.perez@example.com'
        };
        // Setup fetch mock for successful response
        global.fetch.mockResolvedValue({ ok: true });
        // Call createStudent and assert fetch call
        yield studentRepository.createStudent(mockStudent);
        expect(global.fetch).toHaveBeenCalledWith('/SIP/students/api_create_student', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mockStudent)
        });
    }));
    // Test to verify calculation of total pages based on student count
    test('getTotalPages returns the total number of pages', () => __awaiter(void 0, void 0, void 0, function* () {
        // Setup fetch mock with total students count
        global.fetch.mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ total_students: 50 })
        });
        // Call getTotalPages and assert the result
        const totalPages = yield studentRepository.getTotalPages(10);
        expect(totalPages).toBe(5);
    }));
    // Test to verify handling of network errors in getStudent
    test('getStudent handles network errors', () => __awaiter(void 0, void 0, void 0, function* () {
        // Setup fetch mock to simulate network error
        global.fetch.mockRejectedValue(new Error('Network error'));
        // Call getStudent and assert the result
        const student = yield studentRepository.getStudent(1);
        expect(student).toBeNull();
    }));
    // Test to verify handling of network errors in listStudents
    test('listStudents handles network errors', () => __awaiter(void 0, void 0, void 0, function* () {
        // Setup fetch mock to simulate network error
        global.fetch.mockRejectedValue(new Error('Network error'));
        // Call listStudents and assert the result
        const students = yield studentRepository.listStudents(1);
        expect(students).toBeNull();
    }));
    // Test to verify correct API call for updating a student
    test('updateStudent calls fetch with the correct parameters', () => __awaiter(void 0, void 0, void 0, function* () {
        // Define mock student data
        const mockStudent = { id: 1, name: 'Juan', lastname: 'Perez', phone: '1234567890', email: 'juan.perez@example.com' };
        const mockId = 1;
        // Setup fetch mock for successful response
        global.fetch.mockResolvedValue({ ok: true });
        // Call updateStudent and assert fetch call
        yield studentRepository.updateStudent(mockId, mockStudent);
        expect(global.fetch).toHaveBeenCalledWith(`/SIP/students/api_update_student/${mockId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mockStudent)
        });
    }));
    // Test to verify correct API call for deleting a student
    test('deleteStudent calls fetch with the correct parameters', () => __awaiter(void 0, void 0, void 0, function* () {
        // Define mock student id
        const mockId = 1;
        // Setup fetch mock for successful response
        global.fetch.mockResolvedValue({ ok: true });
        // Call deleteStudent and assert fetch call
        yield studentRepository.deleteStudent(mockId);
        expect(global.fetch).toHaveBeenCalledWith(`/SIP/students/api_delete_student/${mockId}`, {
            method: 'DELETE'
        });
    }));
    // Test to verify handling of errors when fetching a student
    test('Handles errors when fetching a student', () => __awaiter(void 0, void 0, void 0, function* () {
        // Setup fetch mock to simulate an error
        global.fetch.mockRejectedValue(new Error('Error al obtener el estudiante'));
        // Spy on alert to capture its call
        const alertSpy = jest.spyOn(window, 'alert');
        // Call getStudent to trigger the error
        yield studentRepository.getStudent(1);
        // Assert that alert was called with the correct message
        expect(alertSpy).toHaveBeenCalledWith('Error al obtener el estudiante: Error: Error al obtener el estudiante');
        // Restore original alert behavior
        alertSpy.mockRestore();
    }));
});
