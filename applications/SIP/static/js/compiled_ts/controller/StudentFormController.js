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
import { StudentFormRenderer } from "../renderer/StudentFormRenderer.js";
import { validateStudent } from "../utils/Validator.js";
export class StudentFormController {
    constructor() {
        this.studentRepository = new StudentRepository();
        this.studentFormRenderer = new StudentFormRenderer();
        this.init();
    }
    init() {
        const formElement = this.studentFormRenderer.render();
        document.body.appendChild(formElement);
    }
    getFormData(form) {
        return {
            name: form.elements.namedItem('name').value,
            lastname: form.elements.namedItem('lastname').value,
            phone: form.elements.namedItem('phone').value,
            email: form.elements.namedItem('email').value
        };
    }
    handleSubmit(event) {
        return __awaiter(this, void 0, void 0, function* () {
            event.preventDefault();
            const form = event.target;
            const studentData = this.getFormData(form);
            const errors = validateStudent(studentData);
            if (errors.length > 0) {
                // Manejar errores de validación aquí
                alert(errors.join("\n"));
                return;
            }
            try {
                yield this.studentRepository.createStudent(studentData);
                alert("Estudiante creado con éxito");
                form.reset();
            }
            catch (error) {
                // Manejar errores del servidor aquí
                alert("Error al crear estudiante");
            }
        });
    }
    bindFormSubmit() {
        const formElement = this.studentFormRenderer.render();
        formElement.onsubmit = (event) => this.handleSubmit(event);
    }
}
