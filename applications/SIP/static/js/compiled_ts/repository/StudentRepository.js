var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
export class StudentRepository {
    getStudent(id) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield fetch(`/SIP/students/api_get_student/${id}`);
                if (!response.ok) {
                    // Maneja la respuesta no exitosa (como 404 o 500)
                    throw new Error('Error al obtener el estudiante');
                }
                const result = yield response.json();
                if (result.status === 'error') {
                    // Maneja el caso de "Student not found" o errores similares
                    console.error(result.message); // O muestra un mensaje al usuario
                    return null;
                }
                return result;
            }
            catch (error) {
                console.error('Error al obtener el estudiante:', error);
                return null;
            }
        });
    }
    listStudents(page) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield fetch(`/SIP/students/api_list_student?page=${page}`);
                if (!response.ok) {
                    throw new Error('Error al obtener la lista de estudiantes');
                }
                const students = yield response.json();
                return students;
            }
            catch (error) {
                console.error('Error al obtener la lista de estudiantes:', error);
                return null;
            }
        });
    }
    createStudent(student) {
        return __awaiter(this, void 0, void 0, function* () {
            yield fetch('/SIP/students/api_create_student', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(student)
            });
        });
    }
    updateStudent(id, student) {
        return __awaiter(this, void 0, void 0, function* () {
            yield fetch(`/SIP/students/api_update_student/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(student)
            });
        });
    }
    deleteStudent(id) {
        return __awaiter(this, void 0, void 0, function* () {
            yield fetch(`/SIP/students/api_delete_student/${id}`, {
                method: 'DELETE'
            });
        });
    }
    getTotalPages(itemsPerPage = 10) {
        return __awaiter(this, void 0, void 0, function* () {
            // Suponiendo que tienes un endpoint que devuelve el total de estudiantes
            const response = yield fetch(`/SIP/students/api_total_students`);
            const totalStudents = yield response.json();
            const totalPages = Math.ceil(totalStudents.total_students / itemsPerPage);
            return totalPages;
        });
    }
}
