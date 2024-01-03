import { Student } from "../models/Student";

export class StudentFactory {
    createStudent(data: Partial<Student>): Student {
        return {
            name: data.name || '',
            lastname: data.lastname || '',
            phone: data.phone || '',
            email: data.email || ''
        };
    }
}