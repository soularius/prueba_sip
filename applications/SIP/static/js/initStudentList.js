import { StudentController } from './compiled_ts/controller/StudentController.js';


document.addEventListener('DOMContentLoaded', function() {
    const studentController = new StudentController();
    const container = document.getElementById('student-list-container');
    studentController.listStudents(container);
});
