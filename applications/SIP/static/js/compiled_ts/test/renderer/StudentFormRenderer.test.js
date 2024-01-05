import { StudentFormRenderer } from '../../renderer/StudentFormRenderer.js';
import { validateStudent } from '../../utils/Validator.js';
import '@testing-library/jest-dom';
jest.mock('../../utils/Validator'); // Mock validation if necessary
// Describes test suite for StudentFormRenderer
describe('StudentFormRenderer', () => {
    let renderer;
    let mockSubmit;
    beforeEach(() => {
        // Initialize the mockSubmit function and the StudentFormRenderer before each test
        mockSubmit = jest.fn();
        renderer = new StudentFormRenderer(mockSubmit);
    });
    // Test to ensure the student form is rendered correctly
    test('should render student form correctly', () => {
        const formElement = renderer.render();
        // Assert that the form element has the correct class and contains the necessary input fields and submit button
        expect(formElement.className).toBe('container mt-3');
        // Verify the presence of the form fields
        const nameInput = formElement.querySelector('input[name="name"]');
        const lastnameInput = formElement.querySelector('input[name="lastname"]');
        const phoneInput = formElement.querySelector('input[name="phone"]');
        const emailInput = formElement.querySelector('input[name="email"]');
        const submitButton = formElement.querySelector('button[type="submit"]');
        // Assert that the form element has the correct class and contains the necessary input fields and submit button
        expect(nameInput).not.toBeNull();
        expect(lastnameInput).not.toBeNull();
        expect(phoneInput).not.toBeNull();
        expect(emailInput).not.toBeNull();
        expect(submitButton).not.toBeNull();
        // Check the text content of the submit button
        if (nameInput && lastnameInput && phoneInput && emailInput && submitButton) {
            expect(submitButton.textContent).toBe('Registrar Estudiante');
        }
    });
    test('should handle form submission with valid data', () => {
        // Mock validation function if needed
        validateStudent.mockReturnValue([]);
        const student = {
            name: 'Laura',
            lastname: 'Gomez',
            phone: '987654321',
            email: 'laura.gomez@example.com'
        };
        const formElement = renderer.render(student);
        const formEvent = new Event('submit');
        // Configure form field values
        formElement.querySelector('input[name="name"]').value = student.name;
        formElement.querySelector('input[name="lastname"]').value = student.lastname;
        formElement.querySelector('input[name="phone"]').value = student.phone;
        formElement.querySelector('input[name="email"]').value = student.email;
        formElement.dispatchEvent(formEvent);
        // Verify that mockSubmit is called with the correct data
        expect(mockSubmit).toHaveBeenCalledWith(student);
    });
});
