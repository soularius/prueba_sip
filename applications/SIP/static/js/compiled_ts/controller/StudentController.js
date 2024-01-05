var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { StudentRepository } from "../repository/StudentRepository.js";
import { StudentListRenderer } from "../renderer/StudentListRenderer.js";
import { StudentDetailsRenderer } from "../renderer/StudentDetailsRenderer.js";
import { StudentEditRenderer } from "../renderer/StudentEditRenderer.js";
import { StudentFormRenderer } from "../renderer/StudentFormRenderer.js";
import { validateStudent } from "../utils/Validator.js";
export class StudentController {
    /**
     * Creates a new instance of the constructor.
     *
     * @param {StudentRepository} [repository] - An optional StudentRepository object. If provided, it will be assigned to the studentRepository property. If not provided, a new StudentRepository object will be created and assigned to the studentRepository property.
     */
    constructor(repository) {
        this.container = null;
        this.currentPage = 1;
        this.studentRepository = repository || new StudentRepository();
        this.studentListRenderer = new StudentListRenderer(this);
        this.studentFormRenderer = new StudentFormRenderer(this.handleCreateStudent.bind(this));
    }
    /**
     * Retrieves the container element.
     *
     * @return {HTMLElement | null} The container element if it exists, otherwise null.
     */
    getContainer() {
        return this.container;
    }
    /**
     * Change the page of the container to the specified page number.
     *
     * @param {number} page - The page number to change to.
     * @return {void} This function does not return anything.
     */
    changePage(page) {
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
    listStudents(container, page = 1) {
        return __awaiter(this, void 0, void 0, function* () {
            this.container = container;
            const students = yield this.studentRepository.listStudents(page);
            if (students) {
                const totalPages = yield this.studentRepository.getTotalPages();
                const listElement = this.studentListRenderer.render(students, page, totalPages, this);
                container.innerHTML = '';
                container.appendChild(listElement);
                this.currentPage = page;
            }
            else {
                container.innerHTML = '<p>Sin Estudiantes registrados.</p>';
            }
        });
    }
    /**
     * Asynchronously displays the details of a student in the specified container.
     *
     * @param {HTMLElement} container - The HTML element where the student details will be displayed.
     * @param {number} id - The ID of the student whose details will be displayed.
     * @return {Promise<void>} - A promise that resolves when the details have been displayed.
     */
    viewDetails(container, id) {
        return __awaiter(this, void 0, void 0, function* () {
            this.container = container;
            const student = yield this.studentRepository.getStudent(id);
            if (student) {
                const detailsRenderer = new StudentDetailsRenderer();
                const detailsElement = detailsRenderer.render(student);
                container.innerHTML = '';
                container.appendChild(detailsElement);
            }
            else {
                container.innerHTML = '<p>Estudiante no encontrado.</p>';
            }
        });
    }
    /**
     * Edits a student by rendering a form to edit their information.
     *
     * @param {HTMLElement} container - The container element where the form will be rendered.
     * @param {number} id - The ID of the student to be edited.
     * @return {Promise<void>} A promise that resolves once the student is edited.
     */
    editStudent(container, id) {
        return __awaiter(this, void 0, void 0, function* () {
            const student = yield this.studentRepository.getStudent(id);
            if (student) {
                const editRenderer = new StudentEditRenderer(this.handleUpdateStudent.bind(this, id));
                const editElement = editRenderer.render(student);
                container.innerHTML = '';
                container.appendChild(editElement);
            }
            else {
                container.innerHTML = '<p>Estudiante no encontrado.</p>';
            }
        });
    }
    /**
     * Deletes a student with the specified ID.
     *
     * @param {number} id - The ID of the student to delete.
     * @return {Promise<void>} - A promise that resolves when the student is deleted successfully.
     */
    deleteStudent(id) {
        return __awaiter(this, void 0, void 0, function* () {
            if (confirm("¿Estás seguro de que deseas eliminar este estudiante?")) {
                try {
                    yield this.studentRepository.deleteStudent(id);
                    alert("Estudiante eliminado con éxito");
                    // Refrescar la lista de estudiantes
                    if (this.container) {
                        // Suponiendo que tienes una variable para mantener la página actual
                        // Si no la tienes, puedes usar un valor predeterminado o implementar la lógica para determinarla                    
                        this.listStudents(this.container, this.currentPage);
                    }
                }
                catch (error) {
                    alert("Error al eliminar estudiante: " + error);
                }
            }
        });
    }
    /**
     * Creates a new student using the provided container element.
     *
     * @param {HTMLElement} container - The HTML element where the form will be rendered.
     * @return {Promise<void>} - A promise that resolves when the student is created successfully.
     */
    createStudent(container) {
        return __awaiter(this, void 0, void 0, function* () {
            const formRenderer = new StudentFormRenderer((studentData) => __awaiter(this, void 0, void 0, function* () {
                try {
                    yield this.studentRepository.createStudent(studentData);
                    alert("Estudiante creado con éxito");
                    // Refresh list or redirect to student list
                }
                catch (error) {
                    alert("Error al crear estudiante");
                }
            }));
            const formElement = formRenderer.render();
            container.innerHTML = '';
            container.appendChild(formElement);
        });
    }
    /**
     * Handles the update of a student.
     *
     * @param {number} id - The ID of the student to be updated.
     * @param {Student} studentData - The updated student data.
     * @return {Promise<void>} - A promise that resolves when the update is complete.
     */
    handleUpdateStudent(id, studentData) {
        return __awaiter(this, void 0, void 0, function* () {
            const errors = validateStudent(studentData);
            if (errors.length > 0) {
                alert(errors.join("\n"));
                return;
            }
            try {
                yield this.studentRepository.updateStudent(id, studentData);
                alert("Estudiante actualizado con éxito");
                // Optional: refresh the list or redirect to another page
            }
            catch (error) {
                alert("Error al actualizar estudiante: " + error);
            }
        });
    }
    /**
     * Handles the creation of a student.
     *
     * @param {Student} studentData - The student data to be created.
     * @return {Promise<void>} A promise that resolves when the student is created.
     */
    handleCreateStudent(studentData) {
        return __awaiter(this, void 0, void 0, function* () {
            const errors = validateStudent(studentData);
            if (errors.length > 0) {
                alert(errors.join("\n"));
                return;
            }
            try {
                yield this.studentRepository.createStudent(studentData);
                alert("Estudiante creado con éxito");
                // Optional: refresh list or redirect to student list
            }
            catch (error) {
                alert("Error al crear estudiante: " + error);
            }
        });
    }
}
