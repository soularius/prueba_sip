export class StudentFactory {
    /**
     * Creates a new student object based on the provided data.
     *
     * @param {Partial<Student>} data - The data to create the student object.
     * @return {Student} The created student object.
     */
    createStudent(data) {
        return {
            name: data.name || '',
            lastname: data.lastname || '',
            phone: data.phone || '',
            email: data.email || ''
        };
    }
}
