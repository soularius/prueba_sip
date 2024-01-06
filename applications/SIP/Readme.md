# School Management System Project

## Project Description

The School Management System is a web application designed to automate and manage key operations in an educational institution. It includes modules for student, teacher, subject, and classroom registration, schedule management, and student attendance tracking, among others.

## Main Features

* Registration of students, teachers, subjects, and classrooms.
* Management of schedules and weekdays.
* Student attendance tracking.
* Data management API.
* Front-end developed in TypeScript and Back-end in Python (web2py).

## System Requirements

* Node.js and npm
* Python 3.x
* PostgreSQL
* Web2py

## Configuration and Installation

1. Clone the repository: `git clone https://github.com/soularius/prueba_sip.git`
2. Install Node.js dependencies: `cd applications/SIP/src && npm install`
3. Configure your Python and PostgreSQL environment.
4. Execute Alembic migrations to set up the database.

### This dependencies for project

#### This for TypeScript

* npm install jest

#### This for Web2py

* pip install psycopg2
* pip install faker
* pip install pydal
* pip install yatl
* pip install gluon
* pip install pyDAL
* pip install requests
* pip install lxml
* pip install pyyaml
* pip install mock

## Compilation and Execution

### TypeScript Compilation

To compile the TypeScript code of the project, follow these steps:

* TypeScript Compilation: Run `npx tsc` to compile the TypeScript files. This will generate the corresponding JavaScript files.
* Post-Processing: Run `node add-js-extension.js` for any necessary post-processing on the generated JavaScript files.

```
> npx tsc && node add-js-extension.js
```

### Test Execution

* TypeScript Tests: To run the TypeScript tests, use the command `npm test`.

```
> cd applications/SIP/src
> npm test
```

* Python Tests (unittest): To execute the Python unit tests, use the following commands:
  * `python -m unittest discover applications/SIP/tests/services/api_services/`
  * Repeat the above command, changing the test directory as necessary (e.g., renderer, models, factory, controller).

```
> cd applications\SIP\
> python -m unittest discover applications\SIP\tests\services\api_services\
> python -m unittest discover applications\SIP\tests\controller\
> python -m unittest discover applications\SIP\tests\factory\
...
```

## Starting the Application

* Web2py: Start the application by running `python web2py.py`.
* Application Access: Once the application is started, access it via [http://127.0.0.1:8000/SIP/](http://127.0.0.1:8000/SIP/). (If use docker deploy [http://127.0.0.1:8080/SIP/](http://127.0.0.1:8080/SIP/) and **the Pass to access admin is 123***)

## Project APIs

The project includes a series of APIs to manage various functionalities. Here are some of them:

### Attendances:

* {{host}}/SIP/attendances/api\_list\_attendance?page=1
* {{host}}/SIP/attendances/api\_get\_attendance/2
* {{host}}/SIP/attendances/api\_update\_attendance/2
* {{host}}/SIP/attendances/api\_delete\_attendance/1
* {{host}}/SIP/attendances/api\_create\_attendance
* {{host}}/SIP/attendances/api\_update\_attendance/2

### Students

* {{host}}/SIP/students/api\_get\_student/1
* {{host}}/SIP/students/api\_list\_student?page=1
* {{host}}/SIP/students/api\_delete\_student/4
* {{host}}/SIP/students/api\_update\_student/5
* {{host}}/SIP/students/api\_create\_student
* {{host}}/SIP/students/api\_total\_students

*All is includes in postman collections*

## Dockerization and Deployment

To facilitate deployment, Dockerfile and docker-compose.yml are included. **Important**: For proper execution in a Docker environment, it is necessary to have SSL certificates and the nginx folder configured.

### Execution with Docker

1. Ensure Docker and Docker Compose are installed.
2. Place your SSL certificates in the `./nginx/certs` folder.
3. Ensure the `./nginx` folder contains the `default.conf` file properly configured.
4. Execute the following command to start the services with Docker Compose:

   <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div></div></pre>
5. <pre><div class="bg-black rounded-md"><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">docker-compose up
   </code></div></div></pre>

   This will start the services defined in `docker-compose.yml`, including the web server, database, and nginx.

*All file is includes in the folder /docker-run (Include one certificate for execution)*

## Code Quality Control

* Use of tools like black, flake8, pylint, bandit (Python), and ESLint (TypeScript).

## Database Configuration

Customize your DB.py file with the following configuration to set up the database connection:

*Note in docker `localhost` is changed to `db`*

<pre><div class="bg-black rounded-md"><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">db = DAL('postgres://postgres:PASS@localhost:5432/sip_ingenieria',
         pool_size=configuration.get('db.pool_size'),
         migrate_enabled=configuration.get('db.migrate'),
         check_reserved=['all'])
</code></div></div></pre>

## Database Visual Model

### Location and Details

* The visual model of the database can be found in the file `modelEnd.svg` located in the `applications/SIP/docs` directory of the project repository.
* This file provides a graphical representation of the database schema, making it easier to understand the structure and relationships between the different tables and entities in the database.

### How to View

* To view the file, simply navigate to the `applications/SIP/docs` directory.
* Open the `modelEnd.svg` file with any compatible SVG viewer or web browser. This will display the visual layout of the database schema.

### Importance of the Visual Model

* Having a visual model is beneficial for both new and existing team members to quickly grasp the database architecture.
* It aids in better understanding the relationships and constraints within the database, which is crucial for effective development and troubleshooting.

## Postman Collections for API Testing

Accessing and Using the Postman Collection

#### Location

The Postman collection is available in the `applications/SIP/test/postman` directory within the project repository.

#### Importing to Postman

1. Open Postman on your computer.
2. Click on the 'Import' button.
3. Choose the file or drag and drop the Postman collection file from the `applications/SIP/test/postman` directory.

#### Using the Collection

1. Once imported, the collection will appear in the left-hand sidebar of Postman.
2. Click on any request to view or edit its details and send requests to the API.
3. Before making requests, ensure to set up your environment in Postman:
   * Go to the 'Manage Environments' section in Postman.
   * Create or select an existing environment.
   * Add a key named `host` and set its value to your local server address or the server hosting the application (e.g., `http://127.0.0.1:8000 or http://127.0.0.1:8080 for docker`).
   * This `host` variable will be used in the collection to refer to the base URL of your API endpoints.
4. Ensure your local server or the server hosting the application is running, as the collection will make requests to the endpoints defined in the collection.

### Benefits of Using Postman Collection

* **Efficiency**: Quickly send requests to the API without manual setup.
* **Consistency**: Ensure that all team members are testing the API in the same way.
* **Documentation**: Serve as a form of live documentation for how the APIs are structured and expected to be used.

### Additional Information

* The Postman collection is regularly updated to reflect any changes or additions to the API.
* Users are encouraged to familiarize themselves with Postman for an efficient testing experience.

## Directory Hierarchy

**This struct is for applications/SIP**

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
|—— docs
|    |—— modelEnd.svg
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
