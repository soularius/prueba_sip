import { Student } from "../models/Student";

export class StudentRepository {
    async getStudent(id: number): Promise<Student> {
        const response = await fetch(`http://127.0.0.1:8000/SIP/students/api_get_student/${id}`);
        return await response.json();
    }

    async listStudents(page: number): Promise<Student[]> {
        const response = await fetch(`http://127.0.0.1:8000/SIP/students/api_list_student?page=${page}`);
        return await response.json();
    }

    async createStudent(student: Student): Promise<void> {
        await fetch('http://127.0.0.1:8000/SIP/students/api_create_student', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(student)
        });
    }

    async updateStudent(id: number, student: Student): Promise<void> {
        await fetch(`http://127.0.0.1:8000/SIP/students/api_update_student/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(student)
        });
    }

    async deleteStudent(id: number): Promise<void> {
        await fetch(`http://127.0.0.1:8000/SIP/students/api_delete_student/${id}`, {
            method: 'DELETE'
        });
    }
}