import { StudentController } from './compiled_ts/controller/StudentController.js';


document.addEventListener('DOMContentLoaded', function() {
    const studentController = new StudentController();
    const container = document.getElementById('student-form-container');
    studentController.createStudent(container);
});
