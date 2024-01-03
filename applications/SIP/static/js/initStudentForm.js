import { StudentFormController } from './compiled_ts/controller/StudentFormController.js';


document.addEventListener('DOMContentLoaded', function() {
    const formController = new StudentFormController();
    formController.bindFormSubmit();
});
