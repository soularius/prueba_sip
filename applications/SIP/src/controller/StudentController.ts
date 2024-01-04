import { StudentRepository } from "../repository/StudentRepository";
import { StudentListRenderer } from "../renderer/StudentListRenderer";
import { StudentDetailsRenderer } from "../renderer/StudentDetailsRenderer";
import { StudentEditRenderer } from "../renderer/StudentEditRenderer";
import { StudentFormRenderer } from "../renderer/StudentFormRenderer";
import { validateStudent } from "../utils/Validator";
import { Student } from "../models/Student";

export class StudentController {
    private studentRepository: StudentRepository;
    private studentListRenderer: StudentListRenderer;
    private studentFormRenderer: StudentFormRenderer;
    private container: HTMLElement | null = null;
    private currentPage: number = 1;

    constructor() {
        this.studentRepository = new StudentRepository();
        this.studentListRenderer = new StudentListRenderer(this);
        this.studentFormRenderer = new StudentFormRenderer(this.handleCreateStudent.bind(this));
    }

    getContainer(): HTMLElement | null {
        return this.container;
    }

    changePage(page: number): void {
        if (this.container) {
            this.listStudents(this.container, page);
        }
    }

    async listStudents(container: HTMLElement, page: number = 1): Promise<void> {
        this.container = container;
        const students = await this.studentRepository.listStudents(page);
        if (students) {
            const totalPages = await this.studentRepository.getTotalPages();
            const listElement = this.studentListRenderer.render(students, page, totalPages, this);
            container.innerHTML = '';
            container.appendChild(listElement);
            this.currentPage = page;
        } else {
            container.innerHTML = '<p>Sin Estudiantes registrados.</p>';
        }
    }

    async viewDetails(container: HTMLElement, id: number): Promise<void> {
        this.container = container;
        const student = await this.studentRepository.getStudent(id);
        if (student) {
            const detailsRenderer = new StudentDetailsRenderer();
            const detailsElement = detailsRenderer.render(student);
            container.innerHTML = '';
            container.appendChild(detailsElement);
        } else {
            container.innerHTML = '<p>Estudiante no encontrado.</p>';
        }
    }

    async editStudent(container: HTMLElement, id: number): Promise<void> {
        const student = await this.studentRepository.getStudent(id);
        if (student) {
            const editRenderer = new StudentEditRenderer(this.handleUpdateStudent.bind(this, id));
            const editElement = editRenderer.render(student);
            container.innerHTML = '';
            container.appendChild(editElement);
        } else {
            container.innerHTML = '<p>Estudiante no encontrado.</p>';
        }
    }

    async deleteStudent(id: number): Promise<void> {
        if (confirm("¿Estás seguro de que deseas eliminar este estudiante?")) {
            try {
                await this.studentRepository.deleteStudent(id);
                alert("Estudiante eliminado con éxito");
                // Refrescar la lista de estudiantes
                if (this.container) {
                    // Suponiendo que tienes una variable para mantener la página actual
                    // Si no la tienes, puedes usar un valor predeterminado o implementar la lógica para determinarla                    
                    this.listStudents(this.container, this.currentPage);
                }
            } catch (error) {
                alert("Error al eliminar estudiante: " + error);
            }
        }
    }

    async createStudent(container: HTMLElement): Promise<void> {
        const formRenderer = new StudentFormRenderer(async (studentData) => {
            try {
                await this.studentRepository.createStudent(studentData);
                alert("Estudiante creado con éxito");
                // Refrescar la lista o redirigir a la lista de estudiantes
            } catch (error) {
                alert("Error al crear estudiante");
            }
        });

        const formElement = formRenderer.render();
        container.innerHTML = '';
        container.appendChild(formElement);
    }

    

    private async handleUpdateStudent(id: number, studentData: Student): Promise<void> {
        const errors = validateStudent(studentData);
        if (errors.length > 0) {
            alert(errors.join("\n"));
            return;
        }

        try {
            await this.studentRepository.updateStudent(id, studentData);
            alert("Estudiante actualizado con éxito");
            // Opcional: refrescar la lista o redirigir a otra página
        } catch (error) {
            alert("Error al actualizar estudiante: " + error);
        }
    }

    private async handleCreateStudent(studentData: Student): Promise<void> {
        const errors = validateStudent(studentData);
        if (errors.length > 0) {
            alert(errors.join("\n"));
            return;
        }

        try {
            await this.studentRepository.createStudent(studentData);
            alert("Estudiante creado con éxito");
            // Opcional: refrescar la lista o redirigir a la lista de estudiantes
        } catch (error) {
            alert("Error al crear estudiante: " + error);
        }
    }
}
