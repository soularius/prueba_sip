import { Student } from "../models/Student";
import { StudentRepository } from "../repository/StudentRepository";
import { StudentFormRenderer } from "../renderer/StudentFormRenderer";
import { validateStudent } from "../utils/Validator";

export class StudentFormController {
    private studentRepository: StudentRepository;
    private studentFormRenderer: StudentFormRenderer;

    constructor() {
        this.studentRepository = new StudentRepository();
        this.studentFormRenderer = new StudentFormRenderer();
        this.init();
    }

    private init(): void {
        const formElement = this.studentFormRenderer.render();
        document.body.appendChild(formElement);
    }

    private getFormData(form: HTMLFormElement): Student {
        return {
            name: (form.elements.namedItem('name') as HTMLInputElement).value,
            lastname: (form.elements.namedItem('lastname') as HTMLInputElement).value,
            phone: (form.elements.namedItem('phone') as HTMLInputElement).value,
            email: (form.elements.namedItem('email') as HTMLInputElement).value
        };
    }

    private async handleSubmit(event: Event): Promise<void> {
        event.preventDefault();
        const form = event.target as HTMLFormElement;
        const studentData = this.getFormData(form);

        const errors = validateStudent(studentData);
        if (errors.length > 0) {
            // Manejar errores de validación aquí
            alert(errors.join("\n"));
            return;
        }

        try {
            await this.studentRepository.createStudent(studentData);
            alert("Estudiante creado con éxito");
            form.reset();
        } catch (error) {
            // Manejar errores del servidor aquí
            alert("Error al crear estudiante");
        }
    }

    public bindFormSubmit(): void {
        const formElement = this.studentFormRenderer.render();
        formElement.onsubmit = (event) => this.handleSubmit(event);
    }
}