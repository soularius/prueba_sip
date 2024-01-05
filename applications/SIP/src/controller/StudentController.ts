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

    /**
     * Creates a new instance of the constructor.
     *
     * @param {StudentRepository} [repository] - An optional StudentRepository object. If provided, it will be assigned to the studentRepository property. If not provided, a new StudentRepository object will be created and assigned to the studentRepository property.
     */
    constructor(repository?: StudentRepository) {
        this.studentRepository = repository || new StudentRepository();
        this.studentListRenderer = new StudentListRenderer(this);
        this.studentFormRenderer = new StudentFormRenderer(this.handleCreateStudent.bind(this));
    }

    /**
     * Retrieves the container element.
     *
     * @return {HTMLElement | null} The container element if it exists, otherwise null.
     */
    getContainer(): HTMLElement | null {
        return this.container;
    }

    /**
     * Change the page of the container to the specified page number.
     *
     * @param {number} page - The page number to change to.
     * @return {void} This function does not return anything.
     */
    changePage(page: number): void {
        if (this.container) {
            this.listStudents(this.container, page);
        }
    }

    /**
     * Asynchronously lists students and renders them in a container element.
     *
     * @param {HTMLElement} container - The container element to render the students in.
     * @param {number} [page=1] - The page number of the students to list (default is 1).
     * @return {Promise<void>} - A promise that resolves when the students are listed and rendered.
     */
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

    /**
     * Asynchronously displays the details of a student in the specified container.
     *
     * @param {HTMLElement} container - The HTML element where the student details will be displayed.
     * @param {number} id - The ID of the student whose details will be displayed.
     * @return {Promise<void>} - A promise that resolves when the details have been displayed.
     */
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

    /**
     * Edits a student by rendering a form to edit their information.
     *
     * @param {HTMLElement} container - The container element where the form will be rendered.
     * @param {number} id - The ID of the student to be edited.
     * @return {Promise<void>} A promise that resolves once the student is edited.
     */
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

    /**
     * Deletes a student with the specified ID.
     *
     * @param {number} id - The ID of the student to delete.
     * @return {Promise<void>} - A promise that resolves when the student is deleted successfully.
     */
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

    /**
     * Creates a new student using the provided container element.
     *
     * @param {HTMLElement} container - The HTML element where the form will be rendered.
     * @return {Promise<void>} - A promise that resolves when the student is created successfully.
     */
    async createStudent(container: HTMLElement): Promise<void> {
        const formRenderer = new StudentFormRenderer(async (studentData) => {
            try {
                await this.studentRepository.createStudent(studentData);
                alert("Estudiante creado con éxito");
                // Refresh list or redirect to student list
            } catch (error) {
                alert("Error al crear estudiante");
            }
        });

        const formElement = formRenderer.render();
        container.innerHTML = '';
        container.appendChild(formElement);
    }

    

    /**
     * Handles the update of a student.
     *
     * @param {number} id - The ID of the student to be updated.
     * @param {Student} studentData - The updated student data.
     * @return {Promise<void>} - A promise that resolves when the update is complete.
     */
    private async handleUpdateStudent(id: number, studentData: Student): Promise<void> {
        const errors = validateStudent(studentData);
        if (errors.length > 0) {
            alert(errors.join("\n"));
            return;
        }

        try {
            await this.studentRepository.updateStudent(id, studentData);
            alert("Estudiante actualizado con éxito");
            // Optional: refresh the list or redirect to another page
        } catch (error) {
            alert("Error al actualizar estudiante: " + error);
        }
    }

    /**
     * Handles the creation of a student.
     *
     * @param {Student} studentData - The student data to be created.
     * @return {Promise<void>} A promise that resolves when the student is created.
     */
    private async handleCreateStudent(studentData: Student): Promise<void> {
        const errors = validateStudent(studentData);
        if (errors.length > 0) {
            alert(errors.join("\n"));
            return;
        }

        try {
            await this.studentRepository.createStudent(studentData);
            alert("Estudiante creado con éxito");
            // Optional: refresh list or redirect to student list
        } catch (error) {
            alert("Error al crear estudiante: " + error);
        }
    }
}
