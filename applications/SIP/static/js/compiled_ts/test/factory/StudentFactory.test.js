import { StudentFactory } from '../../factory/StudentFactory.js';
describe('StudentFactory', () => {
    let factory;
    beforeEach(() => {
        factory = new StudentFactory();
    });
    test('should create a student with all provided data', () => {
        const data = { name: 'Marta', lastname: 'Salcedo', phone: '123456789', email: 'marta@example.com' };
        const student = factory.createStudent(data);
        expect(student).toEqual(data);
    });
    test('should create a student with default values for missing data', () => {
        const data = { name: 'Marta' };
        const student = factory.createStudent(data);
        expect(student).toEqual({
            name: 'Marta',
            lastname: '',
            phone: '',
            email: ''
        });
    });
    test('should create a student with all default values if no data is provided', () => {
        const student = factory.createStudent({});
        expect(student).toEqual({
            name: '',
            lastname: '',
            phone: '',
            email: ''
        });
    });
});
