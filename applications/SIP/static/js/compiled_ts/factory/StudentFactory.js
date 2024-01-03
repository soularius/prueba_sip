export class StudentFactory {
    createStudent(data) {
        return {
            name: data.name || '',
            lastname: data.lastname || '',
            phone: data.phone || '',
            email: data.email || ''
        };
    }
}
