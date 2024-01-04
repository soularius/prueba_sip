import { StudentController } from './compiled_ts/controller/StudentController.js';


document.addEventListener('DOMContentLoaded', function() {
    const studentIdElement = document.getElementById('student_id');
    const studentId = studentIdElement ? studentIdElement.value : null;
    const studentController = new StudentController();
    const container = document.getElementById('student-detail-container');
    studentController.viewDetails(container, studentId);
});
