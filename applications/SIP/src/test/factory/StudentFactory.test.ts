import { StudentFactory } from '../../factory/StudentFactory';

// Describes test suite for StudentFactory
describe('StudentFactory', () => {
  let factory: StudentFactory;

  beforeEach(() => {
    // Initialize the StudentFactory before each test
    factory = new StudentFactory();
  });

  // Test to ensure that a student is created with all provided data
  test('should create a student with all provided data', () => {
    // Define mock data
    const data = { name: 'Marta', lastname: 'Salcedo', phone: '123456789', email: 'marta@example.com' };
    // Create a student using the factory
    const student = factory.createStudent(data);
  
    // Assert that the created student matches the provided data
    expect(student).toEqual(data);
  });

  // Test to check if missing data is replaced with default values
  test('should create a student with default values for missing data', () => {
    // Define partial mock data
    const data = { name: 'Marta' };
    // Create a student using the factory
    const student = factory.createStudent(data);
  
    // Assert that the created student has default values for missing fields
    expect(student).toEqual({
      name: 'Marta',
      lastname: '',
      phone: '',
      email: ''
    });
  });

  // Test to verify that a student is created with default values if no data is provided
  test('should create a student with all default values if no data is provided', () => {
    // Create a student using the factory without providing any data
    const student = factory.createStudent({});
  
    // Assert that the created student has all default values
    expect(student).toEqual({
      name: '',
      lastname: '',
      phone: '',
      email: ''
    });
  });
});
