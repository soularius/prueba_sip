import { validateStudent } from "../utils/Validator.js";
export class StudentEditRenderer {
    constructor(onSubmit) {
        this.formElement = document.createElement('form');
        this.formElement.className = 'container mt-3';
        this.formElement.onsubmit = (event) => this.handleSubmit(event);
        this.onSubmit = onSubmit; // Guarda la función de callback para su uso posterior
    }
    createInputField(name, placeholder, value, type = "text") {
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
    getFormData() {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        const name = (_b = (_a = this.formElement.elements.namedItem('name')) === null || _a === void 0 ? void 0 : _a.value) !== null && _b !== void 0 ? _b : '';
        const lastname = (_d = (_c = this.formElement.elements.namedItem('lastname')) === null || _c === void 0 ? void 0 : _c.value) !== null && _d !== void 0 ? _d : '';
        const phone = (_f = (_e = this.formElement.elements.namedItem('phone')) === null || _e === void 0 ? void 0 : _e.value) !== null && _f !== void 0 ? _f : '';
        const email = (_h = (_g = this.formElement.elements.namedItem('email')) === null || _g === void 0 ? void 0 : _g.value) !== null && _h !== void 0 ? _h : '';
        return { name, lastname, phone, email };
    }
    handleSubmit(event) {
        event.preventDefault();
        const studentData = this.getFormData();
        const errors = validateStudent(studentData);
        if (errors.length > 0) {
            alert(errors.join("\n"));
            return;
        }
        this.onSubmit(studentData); // Llama al callback con los datos del formulario
    }
    render(student) {
        this.formElement.innerHTML = '';
        const fields = [
            { name: 'name', placeholder: 'Nombre', type: 'text', value: student.name },
            { name: 'lastname', placeholder: 'Apellido', type: 'text', value: student.lastname },
            { name: 'phone', placeholder: 'Teléfono', type: 'tel', value: student.phone },
            { name: 'email', placeholder: 'Correo Electrónico', type: 'email', value: student.email }
        ];
        // Iterar y agregar cada campo al formulario
        fields.forEach(field => {
            const inputGroup = this.createInputField(field.name, field.placeholder, field.value, field.type);
            this.formElement.appendChild(inputGroup); // Agrega el grupo de entrada
        });
        // Botón de envío
        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.className = 'btn btn-primary mt-3';
        submitButton.textContent = 'Actualizar Estudiante';
        this.formElement.appendChild(submitButton);
        return this.formElement;
    }
}
