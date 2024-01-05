School Management System Project
Project Description

The School Management System is a web application designed to automate and manage key operations in an educational institution. It includes modules for student, teacher, subject, and classroom registration, schedule management, and student attendance tracking, among others.
Main Features

    Registration of students, teachers, subjects, and classrooms.
    Management of schedules and weekdays.
    Student attendance tracking.
    Data management API.
    Front-end developed in TypeScript and Back-end in Python (web2py).

System Requirements

    Node.js and npm
    Python 3.x
    PostgreSQL
    Web2py

Configuration and Installation

    Clone the repository: git clone [repository URL]
    Install Node.js dependencies: npm install
    Configure your Python and PostgreSQL environment.
    Execute Alembic migrations to set up the database.

Compilation and Execution
TypeScript Compilation

To compile the TypeScript code of the project, follow these steps:

    TypeScript Compilation: Run npx tsc to compile the TypeScript files. This will generate the corresponding JavaScript files.

    Post-Processing: Run node add-js-extension.js for any necessary post-processing on the generated JavaScript files.

Test Execution

    TypeScript Tests: To run the TypeScript tests, use the command npm test.

    Python Tests (unittest)

    To execute the Python unit tests, use the following commands:
        python -m unittest discover applications/SIP/tests/services/api_services/
        Repeat the above command, changing the test directory as necessary (e.g., renderer, models, factory, controller).

Starting the Application

    Web2py: Start the application by running python web2py.py.
    Application Access: Once the application is started, access it via http://127.0.0.1:8000/SIP/.

Project APIs

The project includes a series of APIs to manage various functionalities. Here are some of them:

    Attendance API:
        List attendances: GET http://127.0.0.1:8000/SIP/attendances/api_list_attendance?page=1
        Get specific attendance: GET http://127.0.0.1:8000/SIP/attendances/api_get_attendance/2
        Update attendance: PUT http://127.0.0.1:8000/SIP/attendances/api_update_attendance/2
        Delete attendance: DELETE http://127.0.0.1:8000/SIP/attendances/api_delete_attendance/1
        Create attendance: POST http://127.0.0.1:8000/SIP/attendances/api_create_attendance

    Student API:
        Get specific student: GET http://127.0.0.1:8000/SIP/students/api_get_student/1
        List students: GET http://127.0.0.1:8000/SIP/students/api_list_student?page=1
        Delete student: DELETE http://127.0.0.1:8000/SIP/students/api_delete_student/4
        Update student: PUT http://127.0.0.1:8000/SIP/students/api_update_student/5
        Create student: POST http://127.0.0.1:8000/SIP/students/api_create_student
        Total students: GET http://127.0.0.1:8000/SIP/students/api_total_students

Dockerization and Deployment

    Dockerfile and docker-compose.yml included to facilitate deployment.

Code Quality Control

    Use of tools like black, flake8, pylint, bandit (Python), and ESLint (TypeScript).

Documentation

    All code, comments, and docstrings are in English.
    Follow Python and TypeScript conventions.

Database Configuration

    Customize your DB.py file with the following configuration to set up the database connection:

python

db = DAL('postgres://postgres:PASS@localhost:5432/sip_ingenieria',
         pool_size=configuration.get('db.pool_size'),
         migrate_enabled=configuration.get('db.migrate'),
         check_reserved=['all'])

Postman Collections for API Testing
Note on Postman Collections

As part of the project, we have included a Postman collection to facilitate the testing of APIs. This collection contains pre-configured requests for all the APIs available in the School Management System. It's a valuable tool for developers and testers to quickly test and interact with the API endpoints without the need to manually set up each request.
Accessing and Using the Postman Collection

    Location: The Postman collection is available in the test/postman directory within the project repository.
    Importing to Postman:
        Open Postman on your computer.
        Click on the Import button.
        Choose the file or drag and drop the Postman collection file from the test/postman directory.
    Using the Collection:
        Once imported, the collection will appear in the left-hand sidebar of Postman.
        You can click on any request to view or edit its details and send requests to the API.
        Ensure your local server or the server hosting the application is running, as the collection will make requests to the endpoints defined in the collection.

Benefits of Using Postman Collection

    Efficiency: Quickly send requests to the API without manual setup.
    Consistency: Ensure that all team members are testing the API in the same way.
    Documentation: Serve as a form of live documentation for how the APIs are structured and expected to be used.

Additional Information

    The Postman collection is regularly updated to reflect any changes or additions to the API.
    Users are encouraged to familiarize themselves with Postman for an efficient testing experience.

Directory Hierarchy
```
|—— controllers
|    |—— appadmin.py
|    |—— attendances.py
|    |—— attendances_controller.py
|    |—— classes.py
|    |—— classes_controller.py
|    |—— classes_students.py
|    |—— classes_students_controller.py
|    |—— day_of_weeks.py
|    |—— day_of_weeks_controller.py
|    |—— default.py
|    |—— fake_generate.py
|    |—— fake_generate_controller.py
|    |—— salons.py
|    |—— salons_controller.py
|    |—— schedules.py
|    |—— schedules_controller.py
|    |—— students.py
|    |—— students_controller.py
|    |—— subjects.py
|    |—— subjects_controller.py
|    |—— teachers.py
|    |—— teachers_controller.py
|—— LICENSE
|—— models
|    |—— db.py
|    |—— menu.py
|—— modules
|    |—— factory
|        |—— attendance_factory.py
|        |—— classes_factory.py
|        |—— classes_students_factory.py
|        |—— day_of_week_factory.py
|        |—— salon_factory.py
|        |—— schedule_factory.py
|        |—— singleton_meta.py
|        |—— students_factory.py
|        |—— subject_factory.py
|        |—— teacher_factory.py
|    |—— libs
|    |—— models
|        |—— attendance.py
|        |—— classes.py
|        |—— classes_students.py
|        |—— day_of_week.py
|        |—— salons.py
|        |—— schedules.py
|        |—— student.py
|        |—— subjects.py
|        |—— teachers.py
|    |—— processes
|    |—— renderer
|        |—— renderer_attendance.py
|    |—— repository
|    |—— services
|        |—— api_services
|            |—— api_attendances.py
|            |—— api_students.py
|        |—— business_logic
|    |—— system
|    |—— templates
|    |—— utils
|        |—— fake_data_attendance_generator.py
|        |—— fake_data_classes_generator.py
|        |—— fake_data_classes_students_generator.py
|        |—— fake_data_day_of_week_generator.py
|        |—— fake_data_salons_generator.py
|        |—— fake_data_schedules_generator.py
|        |—— fake_data_student_generator.py
|        |—— fake_data_subjects_generator.py
|        |—— fake_data_teacher_generator.py
|—— src
|    |—— .eslintrc.js
|    |—— add-js-extension.js
|    |—— controller
|        |—— StudentController.ts
|    |—— factory
|        |—— StudentFactory.ts
|    |—— jest.config.js
|    |—— libs
|    |—— models
|        |—— Student.ts
|    |—— package-lock.json
|    |—— package.json
|    |—— processes
|    |—— renderer
|        |—— StudentDetailsRenderer.ts
|        |—— StudentEditRenderer.ts
|        |—— StudentFormRenderer.ts
|        |—— StudentListRenderer.ts
|    |—— repository
|        |—— StudentRepository.ts
|    |—— services
|        |—— api_services
|        |—— business_logic
|    |—— system
|    |—— templates
|    |—— test
|        |—— postman
|            |—— Attendance.postman_collection.json
|            |—— Student.postman_collection.json
|        |—— controller
|            |—— StudentController.test.ts
|        |—— factory
|            |—— StudentFactory.test.ts
|        |—— models
|            |—— Student.test.ts
|        |—— renderer
|            |—— StudentDetailsRenderer.test.ts
|            |—— StudentEditRenderer.test.ts
|            |—— StudentFormRenderer.test.ts
|            |—— StudentListRenderer.test.ts
|        |—— repository
|            |—— StudentRepository.test.ts
|    |—— tsconfig.json
|    |—— utils
|        |—— Validator.ts
|—— static
|    |—— 403.html
|    |—— 404.html
|    |—— 500.html
|    |—— 503.html
|    |—— css
|        |—— bootstrap.min.css
|        |—— bootstrap.min.css.map
|        |—— calendar.css
|        |—— web2py-bootstrap4.css
|        |—— web2py.css
|    |—— images
|        |—— facebook.png
|        |—— favicon.ico
|        |—— favicon.png
|        |—— gplus-32.png
|        |—— twitter.png
|    |—— js
|        |—— analytics.min.js
|        |—— attendanceUpdate.js
|        |—— bootstrap.bundle.min.js
|        |—— bootstrap.bundle.min.js.map
|        |—— calendar.js
|        |—— compiled_ts
|            |—— add-js-extension.js
|            |—— controller
|                |—— StudentController.js
|            |—— factory
|                |—— StudentFactory.js
|            |—— jest.config.js
|            |—— models
|                |—— Student.js
|            |—— renderer
|                |—— StudentDetailsRenderer.js
|                |—— StudentEditRenderer.js
|                |—— StudentFormRenderer.js
|                |—— StudentListRenderer.js
|            |—— repository
|                |—— StudentRepository.js
|            |—— test
|                |—— controller
|                    |—— StudentController.test.js
|                |—— factory
|                    |—— StudentFactory.test.js
|                |—— models
|                    |—— Student.test.js
|                |—— renderer
|                    |—— StudentDetailsRenderer.test.js
|                    |—— StudentEditRenderer.test.js
|                    |—— StudentFormRenderer.test.js
|                    |—— StudentListRenderer.test.js
|                |—— repository
|                    |—— StudentRepository.test.js
|            |—— tsconfig.tsbuildinfo
|            |—— utils
|                |—— Logger.js
|                |—— Validator.js
|        |—— initStudentDetail.js
|        |—— initStudentEdit.js
|        |—— initStudentForm.js
|        |—— initStudentList.js
|        |—— jquery.js
|        |—— modernizr-2.8.3.min.js
|        |—— web2py-bootstrap4.js
|        |—— web2py.js
|—— tests
|    |—— controller
|        |—— test_attendances.py
|        |—— test_attendances_controller.py
|        |—— test_classes_controller.py
|        |—— test_classes_students_controller.py
|        |—— test_day_of_weeks_controller.py
|        |—— test_salons_controller.py
|        |—— test_schedules_controller.py
|        |—— test_students.py
|        |—— test_students_controller.py
|        |—— test_subjects_controller.py
|        |—— test_teachers_controller.py
|    |—— factory
|        |—— test_attendances_factory.py
|        |—— test_classes_factory.py
|        |—— test_classes_students_factory.py
|        |—— test_day_of_week_factory.py
|        |—— test_salon_factory.py
|        |—— test_schedule_factory.py
|        |—— test_students_factory.py
|        |—— test_subject_factory.py
|        |—— test_teacher_factory.py
|    |—— models
|        |—— test_attendance.py
|        |—— test_classes.py
|        |—— test_classes_students.py
|        |—— test_day_of_week.py
|        |—— test_salons.py
|        |—— test_schedules.py
|        |—— test_student.py
|        |—— test_subjects.py
|        |—— test_teachers.py
|    |—— renderer
|        |—— test_renderer_attendance.py
|    |—— services
|        |—— api_services
|            |—— test_api_attendances.py
|            |—— test_api_students.py
|—— uploads
|—— views
|    |—— layout.html
|    |—— students
|        |—— students_edit_ts.html
|        |—— students_list_ts.html
|        |—— students_register_ts.html
|        |—— students_view_ts.html
|    |—— web2py_ajax.html
```