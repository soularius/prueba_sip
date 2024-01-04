import { Student } from "../models/Student";

export class StudentDetailsRenderer {
    render(student: Student): HTMLElement {
        const div = document.createElement('div');
        div.className = 'container mt-3'; // Clase de Bootstrap para contenedor

        // Uso de una tabla Bootstrap para mostrar los detalles
        div.innerHTML = `
            <table class="table table-dark">
                <tbody>
                    <tr>
                        <th scope="row" class="table-active">ID</th>
                        <td>${student.id}</td>
                    </tr>
                    <tr>
                        <th scope="row" class="table-active">Nombre</th>
                        <td>${student.name}</td>
                    </tr>
                    <tr>
                        <th scope="row" class="table-active">Apellido</th>
                        <td>${student.lastname}</td>
                    </tr>
                    <tr>
                        <th scope="row" class="table-active">Teléfono</th>
                        <td>${student.phone}</td>
                    </tr>
                    <tr>
                        <th scope="row" class="table-active">Email</th>
                        <td>${student.email}</td>
                    </tr>
                </tbody>
            </table>
        `;

        return div;
    }
}