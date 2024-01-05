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
    /**
     * Retrieves a student with the given ID from the server.
     *
     * @param {number} id - The ID of the student to retrieve.
     * @return {Promise<Student | null>} A Promise that resolves to the retrieved student, or null
     * if the student is not found.
     */
    getStudent(id) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield fetch(`/SIP/students/api_get_student/${id}`);
                if (!response.ok) {
                    // Handle unsuccessful response (such as 404 or 500)
                    throw new Error('Error al obtener el estudiante');
                }
                const result = yield response.json();
                if (result.status === 'error') {
                    //Handles the case of "Student not found" or similar errors
                    alert(result.message); // Or show a message to the user
                    return null;
                }
                if (result.http_status !== 200)
                    throw new Error(result.http_status);
                return result.student;
            }
            catch (error) {
                alert(`Error al obtener el estudiante: ${error}`);
                return null;
            }
        });
    }
    /**
     * Retrieves a list of students from the API.
     *
     * @param {number} page - The page number to retrieve.
     * @return {Promise<Student[] | null>} A promise that resolves to an array of students, or null if there was an error.
     */
    listStudents(page) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield fetch(`/SIP/students/api_list_student?page=${page}`);
                if (!response.ok) {
                    throw new Error('Error al obtener la lista de estudiantes');
                }
                const data = yield response.json();
                if (data.http_status !== 200) {
                    throw new Error(data.message || 'Error en la respuesta de la API');
                }
                return data.students || [];
            }
            catch (error) {
                alert(`Error al obtener la lista de estudiantes: ${error}`);
                return null;
            }
        });
    }
    /**
     * Creates a student by sending a POST request to the '/SIP/students/api_create_student' endpoint.
     *
     * @param {Student} student - The student object to be created.
     * @return {Promise<void>} - A Promise that resolves when the student is successfully created.
     */
    createStudent(student) {
        return __awaiter(this, void 0, void 0, function* () {
            yield fetch('/SIP/students/api_create_student', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(student)
            });
        });
    }
    /**
     * Updates a student in the database.
     *
     * @param {number} id - The ID of the student to update.
     * @param {Student} student - The updated student object.
     * @return {Promise<void>} A promise that resolves when the update is complete.
     */
    updateStudent(id, student) {
        return __awaiter(this, void 0, void 0, function* () {
            yield fetch(`/SIP/students/api_update_student/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(student)
            });
        });
    }
    /**
     * Deletes a student with the given ID.
     *
     * @param {number} id - The ID of the student to delete.
     * @return {Promise<void>} - A promise that resolves when the deletion is complete.
     */
    deleteStudent(id) {
        return __awaiter(this, void 0, void 0, function* () {
            yield fetch(`/SIP/students/api_delete_student/${id}`, {
                method: 'DELETE'
            });
        });
    }
    /**
     * Retrieves the total number of pages based on the number of items per page.
     *
     * @param {number} itemsPerPage - The number of items to display per page. Default is 50.
     * @return {Promise<number>} - The total number of pages.
     */
    getTotalPages(itemsPerPage = 50) {
        return __awaiter(this, void 0, void 0, function* () {
            // Assuming you have an endpoint that returns the total number of students
            const response = yield fetch(`/SIP/students/api_total_students`);
            const totalStudents = yield response.json();
            const totalPages = Math.ceil(totalStudents.total_students / itemsPerPage);
            return totalPages;
        });
    }
}
