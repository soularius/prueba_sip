import { Student } from "../models/Student";
import { validateStudent } from "../utils/Validator";

export class StudentEditRenderer {
    private formElement: HTMLFormElement;
    private onSubmit: (student: Student) => void;

    /**
     * Creates a new instance of the constructor.
     *
     * @param {Function} onSubmit - The callback function to be executed when the form is submitted.
     */
    constructor(onSubmit: (student: Student) => void) {
        this.formElement = document.createElement('form');
        this.formElement.className = 'container mt-3';
        this.formElement.onsubmit = (event: Event) => this.handleSubmit(event);
        this.onSubmit = onSubmit; // Save the callback function for later use
    }

    /**
     * Creates an input field element with the specified name, placeholder, value, and type.
     *
     * @param {string} name - The name attribute of the input field.
     * @param {string} placeholder - The placeholder text for the input field.
     * @param {string} value - The initial value of the input field.
     * @param {string} [type="text"] - The type of the input field. Defaults to "text".
     * @return {HTMLElement} The created input field element.
     */
    private createInputField(name: string, placeholder: string, value: string, type: string = "text"): HTMLElement {
        const inputGroup = document.createElement('div');
        inputGroup.className = 'form-group';
    
        const input = document.createElement('input');
        input.type = type;
        input.name = name;
        input.placeholder = placeholder;
        input.value = value;
        input.required = true;
        input.className = 'form-control';
    
        inputGroup.appendChild(input);
        return inputGroup;
    }   

    /**
     * Retrieves the form data from the HTML form element.
     *
     * @return {Student} The student object containing the form data.
     */
    private getFormData(): Student {
        const name = (this.formElement.elements.namedItem('name') as HTMLInputElement)?.value ?? '';
        const lastname = (this.formElement.elements.namedItem('lastname') as HTMLInputElement)?.value ?? '';
        const phone = (this.formElement.elements.namedItem('phone') as HTMLInputElement)?.value ?? '';
        const email = (this.formElement.elements.namedItem('email') as HTMLInputElement)?.value ?? '';

        return { name, lastname, phone, email };
    }

    /**
     * Handles the submission of the form.
     *
     * @param {Event} event - The event object representing the form submission.
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
     * Render the student information form.
     *
     * @param {Student} student - The student object containing the information to be rendered.
     * @return {HTMLElement} The rendered form element.
     */
    render(student: Student): HTMLElement {
        this.formElement.innerHTML = '';

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

        //Submit button
        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.className = 'btn btn-primary mt-3';
        submitButton.textContent = 'Actualizar Estudiante';
        this.formElement.appendChild(submitButton);

        return this.formElement;
    }
}
