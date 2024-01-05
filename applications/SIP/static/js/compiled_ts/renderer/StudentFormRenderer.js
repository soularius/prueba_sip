import { validateStudent } from "../utils/Validator.js";
export class StudentFormRenderer {
    /**
     * Constructor for the class.
     *
     * @param {function} onSubmit - The callback function to be executed when the form is submitted.
     */
    constructor(onSubmit) {
        this.formElement = document.createElement('form');
        this.formElement.className = 'container mt-3';
        this.formElement.onsubmit = (event) => this.handleSubmit(event);
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
    createInputField(name, placeholder, value = "", type = "text") {
        const inputGroup = document.createElement('div');
        inputGroup.className = 'form-group';
        const input = document.createElement('input');
        input.type = type;
        input.name = name;
        input.placeholder = placeholder;
        input.value = value; // Value assignment is added
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
    getFormData() {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        const name = (_b = (_a = this.formElement.elements.namedItem('name')) === null || _a === void 0 ? void 0 : _a.value) !== null && _b !== void 0 ? _b : '';
        const lastname = (_d = (_c = this.formElement.elements.namedItem('lastname')) === null || _c === void 0 ? void 0 : _c.value) !== null && _d !== void 0 ? _d : '';
        const phone = (_f = (_e = this.formElement.elements.namedItem('phone')) === null || _e === void 0 ? void 0 : _e.value) !== null && _f !== void 0 ? _f : '';
        const email = (_h = (_g = this.formElement.elements.namedItem('email')) === null || _g === void 0 ? void 0 : _g.value) !== null && _h !== void 0 ? _h : '';
        return { name, lastname, phone, email };
    }
    /**
     * Handles the form submission event.
     *
     * @param {Event} event - The event object for the form submission.
     * @return {void} This function does not return a value.
     */
    handleSubmit(event) {
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
    render(student = { name: '', lastname: '', phone: '', email: '' }) {
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
