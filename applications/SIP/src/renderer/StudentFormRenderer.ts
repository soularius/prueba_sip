import { Student } from "../models/Student";
import { validateStudent } from "../utils/Validator";

export class StudentFormRenderer {
    private formElement: HTMLFormElement;
    private onSubmit: (student: Student) => void;

    /**
     * Constructor for the class.
     *
     * @param {function} onSubmit - The callback function to be executed when the form is submitted.
     */
    constructor(onSubmit: (student: Student) => void) {
        this.formElement = document.createElement('form');
        this.formElement.className = 'container mt-3';
        this.formElement.onsubmit = (event: Event) => this.handleSubmit(event);
        this.onSubmit = onSubmit;
    }

    /**
     * Creates an input field element with the specified name, placeholder, value, and type.
     *
     * @param {string} name - The name of the input field.
     * @param {string} placeholder - The placeholder text for the input field.
     * @param {string} [value=""] - The initial value of the input field. Default is an empty string.
     * @param {string} [type="text"] - The type of the input field. Default is "text".
     * @return {HTMLElement} - The created input field element.
     */
    private createInputField(name: string, placeholder: string, value: string = "", type: string = "text"): HTMLElement {
        const inputGroup = document.createElement('div');
        inputGroup.className = 'form-group';

        const input = document.createElement('input');
        input.type = type;
        input.name = name;
        input.placeholder = placeholder;
        input.value = value;  // Value assignment is added
        input.required = true;
        input.className = 'form-control';

        inputGroup.appendChild(input);
        return inputGroup;
    }

    /**
     * Retrieves the form data from the HTML form and returns it as a Student object.
     *
     * @return {Student} The form data as a Student object.
     */
    private getFormData(): Student {
        const name = (this.formElement.elements.namedItem('name') as HTMLInputElement)?.value ?? '';
        const lastname = (this.formElement.elements.namedItem('lastname') as HTMLInputElement)?.value ?? '';
        const phone = (this.formElement.elements.namedItem('phone') as HTMLInputElement)?.value ?? '';
        const email = (this.formElement.elements.namedItem('email') as HTMLInputElement)?.value ?? '';

        return { name, lastname, phone, email };
    }

    /**
     * Handles the form submission event.
     *
     * @param {Event} event - The event object for the form submission.
     * @return {void} This function does not return a value.
     */
    private handleSubmit(event: Event): void {
        event.preventDefault();
        const studentData = this.getFormData();
        const errors = validateStudent(studentData);
        if (errors.length > 0) {
            alert(errors.join("\n"));
            return;
        }
        this.onSubmit(studentData); // Call the callback with the form data
    }

    /**
     * Renders the form element with the provided student data or with empty fields if no student is provided.
     *
     * @param {Student} [student] - The student object with the properties: name, lastname, phone, email.
     * @return {HTMLElement} - The rendered form element.
     */
    render(student: Student = { name: '', lastname: '', phone: '', email: '' }): HTMLElement {
        this.formElement.innerHTML = '';

        // Definir los campos del formulario
        const fields = [
            { name: 'name', placeholder: 'Nombre', type: 'text', value: student.name },
            { name: 'lastname', placeholder: 'Apellido', type: 'text', value: student.lastname },
            { name: 'phone', placeholder: 'Teléfono', type: 'tel', value: student.phone },
            { name: 'email', placeholder: 'Correo Electrónico', type: 'email', value: student.email }
        ];

        // Iterate and add each field to the form
        fields.forEach(field => {
            const inputGroup = this.createInputField(field.name, field.placeholder, field.value, field.type);
            this.formElement.appendChild(inputGroup); // Add the input group
        });

        // Submit button
        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.className = 'btn btn-primary mt-3';
        submitButton.textContent = 'Registrar Estudiante';
        this.formElement.appendChild(submitButton);

        return this.formElement;
    }
}