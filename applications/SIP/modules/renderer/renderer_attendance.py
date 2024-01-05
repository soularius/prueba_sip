from gluon.html import TABLE, TR, TH, TD, SELECT, OPTION, URL

class RendererAttendance:
    """
    Class for rendering attendance views into an HTML table.

    This class takes attendance records and transforms them into an HTML table,
    displaying details like the student's name, classroom, subject, and controls
    for updating the attendance status.

    Attributes:
        db: An instance of the database, used for making queries.

    Methods:
        render_view(attendance_records): Takes a list of attendance records and returns an HTML table.
        get_student_name(classes_students_record): Returns the full name of the student given a classes_students record.
        get_salon_name(classes_students_record): Returns the name of the classroom given a classes_students record.
        get_subject_name(classes_students_record): Returns the name of the subject given a classes_students record.
    """
    def __init__(self, db):
        """
        Initializes the RendererAttendance class with a database instance.

        Args:
            db: An instance of the database.
        """
        self.db = db

    def render_view(self, attendance_records):
        """
        Renders a view of attendance records as an HTML table.

        Takes a list of attendance records and transforms them into an HTML table.
        Each row of the table represents an attendance record, displaying details
        such as the student's name, classroom, subject, and controls for updating
        the attendance status.

        Args:
            attendance_records: A list of attendance records to be displayed in the table.

        Returns:
            A TABLE instance containing formatted attendance records for display.
        """
        rows = [TR(TH("ID"), TH("Estudiante"), TH("Salón"), TH("Materia"), TH("Asistencia PY"), TH("Asistencia API"))]

        for record in attendance_records:
            # Here, record is a Row instance of the attendance table

            current_status = str(record.status)
            # Get the associated classes_students record
            classes_students_record = self.db.classes_students(record.classes_students_id)
            # Get details of each record
            student_name = self.get_student_name(classes_students_record)
            salon_name = self.get_salon_name(classes_students_record)
            subject_name = self.get_subject_name(classes_students_record)

            ajax_url = URL('attendances', 'attendance_update', args=[record.id], extension='json')
            # Create queue with select control for attendance
            attendance_select = SELECT(
                OPTION("✔️", _value="1", _selected=current_status == "1"),
                OPTION("❌", _value="0", _selected=current_status == "0"),
                _name=f"status_{record.id}",
                _onchange=f"ajax('{ajax_url}', ['status_{record.id}'], ':eval')"
            );

            attendance_select_API = SELECT(
                OPTION("✔️", _value="1", _selected=current_status == "1"),
                OPTION("❌", _value="0", _selected=current_status == "0"),
                _name=f"status_ajax_{record.id}",
                _onchange=f"updateAttendanceStatus({record.id}, this.value)"
            )

            row = TR(TD(record.id), TD(student_name), TD(salon_name), TD(subject_name), TD(attendance_select), TD(attendance_select_API))
            rows.append(row)            

        return TABLE(*rows, _class="table")

    def get_student_name(self, classes_students_record):
        """
        Retrieves the full name of the student from a classes_students record.

        Args:
            classes_students_record: A record from the classes_students table, which
                                     contains the student's ID.

        Returns:
            The full name of the student as a string. Returns "N/A" if the student is not found.
        """
        # Get student record using student ID
        student_record = self.db.students(classes_students_record.student_id)
        if student_record:
            return f"{student_record.name} {student_record.lastname}"
        else:
            return "N/A"

    def get_salon_name(self, classes_students_record):
        """
        Retrieves the name of the classroom from a classes_students record.

        Args:
            classes_students_record: A record from the classes_students table, which
                                     contains the class ID and, hence, the classroom ID.

        Returns:
            The name of the classroom as a string. Returns "N/A" if the classroom is not found.
        """
        # Get the class registration to access the room ID
        class_record = self.db.classes(classes_students_record.classes_id)
        if class_record:
            salon_record = self.db.salons(class_record.salon_id)
            return salon_record.name if salon_record else "N/A"
        else:
            return "N/A"

    def get_subject_name(self, classes_students_record):
        """
        Retrieves the name of the subject from a classes_students record.

        Args:
            classes_students_record: A record from the classes_students table, which
                                     contains the class ID and, hence, the subject ID.

        Returns:
            The name of the subject as a string. Returns "N/A" if the subject is not found.
        """
        # Get the class record to access the subject ID
        class_record = self.db.classes(classes_students_record.classes_id)
        if class_record:
            subject_record = self.db.subjects(class_record.subject_id)
            return subject_record.name if subject_record else "N/A"
        else:
            return "N/A"