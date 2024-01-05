import { StudentFormRenderer } from '../../renderer/StudentFormRenderer.js';
import { validateStudent } from '../../utils/Validator.js';
import '@testing-library/jest-dom';
jest.mock('../../utils/Validator'); // Mockear la validación si es necesario
describe('StudentFormRenderer', () => {
    let renderer;
    let mockSubmit;
    beforeEach(() => {
        mockSubmit = jest.fn();
        renderer = new StudentFormRenderer(mockSubmit);
    });
    test('should render student form correctly', () => {
        const formElement = renderer.render();
        expect(formElement.className).toBe('container mt-3');
        // Verificar la presencia de los campos del formulario
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
            expect(submitButton.textContent).toBe('Registrar Estudiante');
        }
    });
    test('should handle form submission with valid data', () => {
        // Mock de la función de validación si es necesario
        validateStudent.mockReturnValue([]);
        const student = {
            name: 'Laura',
            lastname: 'Gomez',
            phone: '987654321',
            email: 'laura.gomez@example.com'
        };
        const formElement = renderer.render(student);
        const formEvent = new Event('submit');
        // Configurar los valores de los campos del formulario
        formElement.querySelector('input[name="name"]').value = student.name;
        formElement.querySelector('input[name="lastname"]').value = student.lastname;
        formElement.querySelector('input[name="phone"]').value = student.phone;
        formElement.querySelector('input[name="email"]').value = student.email;
        formElement.dispatchEvent(formEvent);
        // Verificar que se llame a mockSubmit con los datos correctos
        expect(mockSubmit).toHaveBeenCalledWith(student);
    });
});
