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
    constructor(repository) {
        this.container = null;
        this.currentPage = 1;
        this.studentRepository = repository || new StudentRepository();
        this.studentListRenderer = new StudentListRenderer(this);
        this.studentFormRenderer = new StudentFormRenderer(this.handleCreateStudent.bind(this));
    }
    getContainer() {
        return this.container;
    }
    changePage(page) {
        if (this.container) {
            this.listStudents(this.container, page);
        }
    }
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
    createStudent(container) {
        return __awaiter(this, void 0, void 0, function* () {
            const formRenderer = new StudentFormRenderer((studentData) => __awaiter(this, void 0, void 0, function* () {
                try {
                    yield this.studentRepository.createStudent(studentData);
                    alert("Estudiante creado con éxito");
                    // Refrescar la lista o redirigir a la lista de estudiantes
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
                // Opcional: refrescar la lista o redirigir a otra página
            }
            catch (error) {
                alert("Error al actualizar estudiante: " + error);
            }
        });
    }
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
                // Opcional: refrescar la lista o redirigir a la lista de estudiantes
            }
            catch (error) {
                alert("Error al crear estudiante: " + error);
            }
        });
    }
}
