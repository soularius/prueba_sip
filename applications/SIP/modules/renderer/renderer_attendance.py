from gluon.html import TABLE, TR, TH, TD, SELECT, OPTION, URL

class RendererAttendance:
    def __init__(self, db):
        self.db = db

    def render_view(self, attendance_records):
        rows = [TR(TH("ID"), TH("Estudiante"), TH("Salón"), TH("Materia"), TH("Asistencia PY"), TH("Asistencia API"))]

        for record in attendance_records:
            # Aquí, record es una instancia de Row de la tabla attendance

            current_status = str(record.status)
            # Obtener el registro classes_students asociado
            classes_students_record = self.db.classes_students(record.classes_students_id)

            # Obtener detalles de cada registro
            student_name = self.get_student_name(classes_students_record)
            salon_name = self.get_salon_name(classes_students_record)
            subject_name = self.get_subject_name(classes_students_record)

            ajax_url = URL('attendances', 'attendance_update', args=[record.id], extension='json')
            # Crear fila con control select para asistencia
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
        # Obtener el registro del estudiante usando el ID del estudiante
        student_record = self.db.students(classes_students_record.student_id)
        if student_record:
            return f"{student_record.name} {student_record.lastname}"
        else:
            return "N/A"

    def get_salon_name(self, classes_students_record):
        # Obtener el registro de la clase para acceder al ID del salón
        class_record = self.db.classes(classes_students_record.classes_id)
        if class_record:
            salon_record = self.db.salons(class_record.salon_id)
            return salon_record.name if salon_record else "N/A"
        else:
            return "N/A"

    def get_subject_name(self, classes_students_record):
        # Obtener el registro de la clase para acceder al ID de la materia
        class_record = self.db.classes(classes_students_record.classes_id)
        if class_record:
            subject_record = self.db.subjects(class_record.subject_id)
            return subject_record.name if subject_record else "N/A"
        else:
            return "N/A"