import { Student } from "../models/Student";
export class StudentRepository {
    async getStudent(id: number): Promise<Student | null> {
        try {
            const response = await fetch(`/SIP/students/api_get_student/${id}`);
            if (!response.ok) {
                // Maneja la respuesta no exitosa (como 404 o 500)
                throw new Error('Error al obtener el estudiante');
            }
            const result = await response.json();
            if (result.status === 'error') {
                // Maneja el caso de "Student not found" o errores similares
                alert(result.message); // O muestra un mensaje al usuario
                return null;
            }
            if(result.http_status !== 200) throw new Error(result.http_status)
            return result.student;
        } catch (error) {
            alert(`Error al obtener el estudiante: ${error}`);
            return null;
        }
    }

    async listStudents(page: number): Promise<Student[] | null> {
        try {
            const response = await fetch(`/SIP/students/api_list_student?page=${page}`);
            if (!response.ok) {
                throw new Error('Error al obtener la lista de estudiantes');
            }
            const data = await response.json();
            if (data.http_status !== 200) {
                throw new Error(data.message || 'Error en la respuesta de la API');
            }
            return data.students || [];
        } catch (error) {
            alert(`Error al obtener la lista de estudiantes: ${error}`);
            return null;
        }
    }

    async createStudent(student: Student): Promise<void> {
        await fetch('/SIP/students/api_create_student', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(student)
        });
    }

    async updateStudent(id: number, student: Student): Promise<void> {
        await fetch(`/SIP/students/api_update_student/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(student)
        });
    }

    async deleteStudent(id: number): Promise<void> {
        await fetch(`/SIP/students/api_delete_student/${id}`, {
            method: 'DELETE'
        });
    }

    async getTotalPages(itemsPerPage: number = 50): Promise<number> {
        // Suponiendo que tienes un endpoint que devuelve el total de estudiantes
        const response = await fetch(`/SIP/students/api_total_students`);
        const totalStudents = await response.json();
        const totalPages = Math.ceil(totalStudents.total_students / itemsPerPage);
        return totalPages;
    }
}