import { Student } from "../models/Student";
import { validateStudent } from "../utils/Validator";

export class StudentEditRenderer {
    private formElement: HTMLFormElement;
    private onSubmit: (student: Student) => void;

    constructor(onSubmit: (student: Student) => void) {
        this.formElement = document.createElement('form');
        this.formElement.className = 'container mt-3';
        this.formElement.onsubmit = (event: Event) => this.handleSubmit(event);
        this.onSubmit = onSubmit; // Guarda la función de callback para su uso posterior
    }

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

    private getFormData(): Student {
        const name = (this.formElement.elements.namedItem('name') as HTMLInputElement)?.value ?? '';
        const lastname = (this.formElement.elements.namedItem('lastname') as HTMLInputElement)?.value ?? '';
        const phone = (this.formElement.elements.namedItem('phone') as HTMLInputElement)?.value ?? '';
        const email = (this.formElement.elements.namedItem('email') as HTMLInputElement)?.value ?? '';

        return { name, lastname, phone, email };
    }

    private handleSubmit(event: Event): void {
        event.preventDefault();
        const studentData = this.getFormData();
        const errors = validateStudent(studentData);
        if (errors.length > 0) {
            alert(errors.join("\n"));
            return;
        }
        this.onSubmit(studentData); // Llama al callback con los datos del formulario
    }

    render(student: Student): HTMLElement {
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
