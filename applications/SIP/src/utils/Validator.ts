import { Student } from "../models/Student";

export const validateStudent = (student: Student): string[] => {
    const errors: string[] = [];
    
    if (!student.name) errors.push("El nombre es obligatorio");

    return errors;
};
