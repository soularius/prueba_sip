import { StudentEditRenderer } from '../../renderer/StudentEditRenderer.js';
import { validateStudent } from '../../utils/Validator.js';
import '@testing-library/jest-dom';
jest.mock('../../utils/Validator'); // Mock the Validator if necessary
// Describes test suite for StudentEditRenderer
describe('StudentEditRenderer', () => {
    let renderer;
    let mockSubmit;
    beforeEach(() => {
        // Initialize the mockSubmit function and the StudentEditRenderer before each test
        mockSubmit = jest.fn();
        renderer = new StudentEditRenderer(mockSubmit);
    });
    // Test to ensure the edit form is rendered correctly with student data
    test('should render edit form with student data', () => {
        // Define a mock student object
        const student = {
            name: 'Juan',
            lastname: 'Perez',
            phone: '123456789',
            email: 'juan.perez@example.com'
        };
        // Render edit form using the renderer
        const formElement = renderer.render(student);
        // Assert that the form element has the correct class and contains expected content
        expect(formElement.className).toBe('container mt-3');
        // Check values of input fields and button text
        const nameInput = formElement.querySelector('input[name="name"]');
        const lastnameInput = formElement.querySelector('input[name="lastname"]');
        const phoneInput = formElement.querySelector('input[name="phone"]');
        const emailInput = formElement.querySelector('input[name="email"]');
        const submitButton = formElement.querySelector('button[type="submit"]');
        expect(nameInput).not.toBeNull();
        expect(lastnameInput).not.toBeNull();
        expect(phoneInput).not.toBeNull();
        expect(emailInput).not.toBeNull();
        expect(submitButton).not.toBeNull();
        if (nameInput && lastnameInput && phoneInput && emailInput && submitButton) {
            expect(nameInput.value).toBe('Juan');
            expect(lastnameInput.value).toBe('Perez');
            expect(phoneInput.value).toBe('123456789');
            expect(emailInput.value).toBe('juan.perez@example.com');
            expect(submitButton.textContent).toBe('Actualizar Estudiante');
        }
    });
    test('should handle form submission', () => {
        // Mock de la función de validación si es necesario
        validateStudent.mockReturnValue([]);
        // Define a mock student object
        const student = {
            name: 'Laura',
            lastname: 'Gomez',
            phone: '987654321',
            email: 'laura.gomez@example.com'
        };
        // Render edit form and simulate form submission
        const formElement = renderer.render(student);
        const formEvent = new Event('submit');
        formElement.dispatchEvent(formEvent);
        // Verify that mockSubmit is called with the correct data
        expect(mockSubmit).toHaveBeenCalledWith(student);
    });
});
