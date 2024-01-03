export const validateStudent = (student) => {
    const errors = [];
    if (!student.name)
        errors.push("El nombre es obligatorio");
    return errors;
};
