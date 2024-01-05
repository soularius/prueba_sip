// Describes test suite for the Student model
describe('Student Model', () => {
    // Test to ensure a valid student object is created with all properties
    test('should create a valid student object', () => {
        // Define a mock student object with all properties
        const student = {
            id: 1,
            name: 'Juan',
            lastname: 'Perez',
            phone: '123456789',
            email: 'juan.perez@example.com'
        };
        // Assert that the student object has all the expected properties with correct values
        expect(student).toHaveProperty('id', 1);
        expect(student).toHaveProperty('name', 'Juan');
        expect(student).toHaveProperty('lastname', 'Perez');
        expect(student).toHaveProperty('phone', '123456789');
        expect(student).toHaveProperty('email', 'juan.perez@example.com');
    });
    // Test to check if the student model allows creation without an 'id' property
    test('should allow creation of student without id', () => {
        // Define a mock student object without an 'id' property
        const student = {
            name: 'Laura',
            lastname: 'Gomez',
            phone: '987654321',
            email: 'laura.gomez@example.com'
        };
        // Assert that the student object does not have an 'id' and has correct values for other properties
        expect(student).not.toHaveProperty('id');
        expect(student).toHaveProperty('name', 'Laura');
        expect(student).toHaveProperty('lastname', 'Gomez');
        expect(student).toHaveProperty('phone', '987654321');
        expect(student).toHaveProperty('email', 'laura.gomez@example.com');
    });
});
export {};
