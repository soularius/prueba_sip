import { Student } from "../models/Student";

export const validateStudent = (student: Student): string[] => {
    const errors: string[] = [];
    
    if (!student.name.trim()) {
        errors.push("El nombre es obligatorio.");
    }

    if (!student.lastname.trim()) {
        errors.push("El apellido es obligatorio.");
    }

    if (!student.phone.trim()) {
        errors.push("El teléfono es obligatorio.");
    } else if (!/^\d{7,10}$/.test(student.phone)) {
        // Suponiendo un número telefónico de entre 7 y 10 dígitos
        errors.push("El teléfono debe tener entre 7 y 10 dígitos.");
    }

    if (!student.email.trim()) {
        errors.push("El correo electrónico es obligatorio.");
    } else if (!/\S+@\S+\.\S+/.test(student.email)) {
        // Validación simple de formato de correo electrónico
        errors.push("El correo electrónico no tiene un formato válido.");
    }

    return errors;
};
