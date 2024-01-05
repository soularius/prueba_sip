import { StudentEditRenderer } from '../../renderer/StudentEditRenderer.js';
import { validateStudent } from '../../utils/Validator.js';
import '@testing-library/jest-dom';
jest.mock('../../utils/Validator'); // Si es necesario mockear la validación
describe('StudentEditRenderer', () => {
    let renderer;
    let mockSubmit;
    beforeEach(() => {
        mockSubmit = jest.fn();
        renderer = new StudentEditRenderer(mockSubmit);
    });
    test('should render edit form with student data', () => {
        const student = {
            name: 'Juan',
            lastname: 'Perez',
            phone: '123456789',
            email: 'juan.perez@example.com'
        };
        const formElement = renderer.render(student);
        expect(formElement.className).toBe('container mt-3');
        // Verificar que los elementos existen antes de probar sus propiedades
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
        const student = {
            name: 'Laura',
            lastname: 'Gomez',
            phone: '987654321',
            email: 'laura.gomez@example.com'
        };
        const formElement = renderer.render(student);
        const formEvent = new Event('submit');
        formElement.dispatchEvent(formEvent);
        // Verifica que se llame a mockSubmit con los datos correctos
        expect(mockSubmit).toHaveBeenCalledWith(student);
    });
});
