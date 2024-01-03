import { Student } from "../models/Student";

export class StudentFormRenderer {
    private formElement: HTMLFormElement;

    constructor() {
        this.formElement = document.createElement('form');
        this.formElement.onsubmit = (event: Event) => this.handleSubmit(event);
    }

    private createInputField(name: string, placeholder: string, type: string = "text"): HTMLInputElement {
        const input = document.createElement('input');
        input.type = type;
        input.name = name;
        input.placeholder = placeholder;
        input.required = true;
        return input;
    }

    private handleSubmit(event: Event): void {
        event.preventDefault();
        // Aquí puedes añadir lógica adicional para manejar el envío del formulario
        console.log("Form Submitted");
    }

    render(student: Student = { name: '', lastname: '', phone: '', email: '' }): HTMLElement {
        this.formElement.innerHTML = '';
        this.formElement.className = 'form container';

        // Definir los campos del formulario
        const fields = [
            { name: 'name', placeholder: 'Nombre', type: 'text', value: student.name },
            { name: 'lastname', placeholder: 'Apellido', type: 'text', value: student.lastname },
            { name: 'phone', placeholder: 'Teléfono', type: 'tel', value: student.phone },
            { name: 'email', placeholder: 'Correo Electrónico', type: 'email', value: student.email }
        ];

        // Iterar y agregar cada campo al formulario
        fields.forEach(field => {
            const input = this.createInputField(field.name, field.placeholder, field.type);
            input.value = field.value;
            input.className = 'form-control';

            const divBox = document.createElement('div');
            divBox.className = 'mb-3';
            divBox.appendChild(input);

            this.formElement.appendChild(divBox);
        });

        // Botón de envío
        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.className = 'btn btn-primary';
        submitButton.textContent = 'Registrar Estudiante';
        this.formElement.appendChild(submitButton);

        return this.formElement;
    }
}