describe('Student Model', () => {
    test('should create a valid student object', () => {
        const student = {
            id: 1,
            name: 'Juan',
            lastname: 'Perez',
            phone: '123456789',
            email: 'juan.perez@example.com'
        };
        expect(student).toHaveProperty('id', 1);
        expect(student).toHaveProperty('name', 'Juan');
        expect(student).toHaveProperty('lastname', 'Perez');
        expect(student).toHaveProperty('phone', '123456789');
        expect(student).toHaveProperty('email', 'juan.perez@example.com');
    });
    test('should allow creation of student without id', () => {
        const student = {
            name: 'Laura',
            lastname: 'Gomez',
            phone: '987654321',
            email: 'laura.gomez@example.com'
        };
        expect(student).not.toHaveProperty('id');
        expect(student).toHaveProperty('name', 'Laura');
        expect(student).toHaveProperty('lastname', 'Gomez');
        expect(student).toHaveProperty('phone', '987654321');
        expect(student).toHaveProperty('email', 'laura.gomez@example.com');
    });
});
export {};
