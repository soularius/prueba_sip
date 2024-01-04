export class StudentListRenderer {
    constructor(studentController) {
        this.studentController = studentController;
    }
    render(students, currentPage, totalPages, studentController) {
        const divContent = document.createElement('div');
        divContent.className = 'container';
        const table = document.createElement('table');
        table.className = 'table'; // Clase de Bootstrap
        // Añadir encabezado de tabla
        const thead = table.createTHead();
        const row = thead.insertRow();
        const headers = ['ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Acciones'];
        headers.forEach(text => {
            const th = document.createElement('th');
            th.textContent = text;
            th.className = 'text-center';
            row.appendChild(th);
        });
        // Añadir filas de tabla
        const tbody = table.createTBody();
        students.forEach(student => {
            const tr = tbody.insertRow();
            tr.innerHTML = `
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.lastname}</td>
                <td>${student.phone}</td>
                <td>${student.email}</td>          
            `;
            const actionsTd = document.createElement('td');
            const viewLink = document.createElement('a');
            viewLink.href = `/SIP/students/students_view_ts/${student.id}`;
            viewLink.className = 'btn btn-primary btn-sm mr-2';
            viewLink.textContent = 'Ver';
            actionsTd.appendChild(viewLink);
            const editLink = document.createElement('a');
            editLink.href = `/SIP/students/students_edit_ts/${student.id}`;
            editLink.className = 'btn btn-info btn-sm mr-2';
            editLink.textContent = 'Editar';
            actionsTd.appendChild(editLink);
            const deleteButton = document.createElement('button');
            deleteButton.className = 'btn btn-danger btn-sm';
            deleteButton.textContent = 'Eliminar';
            const studentId = student.id;
            if (typeof studentId === 'number') {
                deleteButton.onclick = () => {
                    studentController.deleteStudent(studentId);
                };
            }
            actionsTd.appendChild(deleteButton);
            actionsTd.className = 'text-center';
            tr.appendChild(actionsTd);
        });
        divContent.appendChild(table);
        const pagination = this.createPagination(currentPage, totalPages, studentController);
        divContent.appendChild(pagination);
        return divContent;
    }
    handleViewClick(id) {
        const container = this.studentController.getContainer();
        console.log(container);
        if (container)
            this.studentController.viewDetails(container, id);
    }
    handleEditClick(id) {
        const container = this.studentController.getContainer();
        if (container)
            this.studentController.editStudent(container, id);
    }
    handleDeleteClick(id) {
        const container = this.studentController.getContainer();
        if (container)
            this.studentController.deleteStudent(id);
    }
    createPagination(currentPage, totalPages, studentController) {
        const nav = document.createElement('nav');
        nav.setAttribute('aria-label', 'Page navigation example');
        const ul = document.createElement('ul');
        ul.className = 'pagination';
        // Botón para ir a la página anterior
        const prevLi = document.createElement('li');
        prevLi.className = 'page-item';
        const prevLink = document.createElement('a');
        prevLink.className = 'page-link';
        prevLink.href = '#';
        prevLink.setAttribute('aria-label', 'Previous');
        prevLink.innerHTML = '<span aria-hidden="true">&laquo;</span>';
        prevLink.onclick = () => {
            if (currentPage > 1)
                studentController.changePage(currentPage - 1);
        };
        prevLi.appendChild(prevLink);
        ul.appendChild(prevLi);
        // Números de página
        for (let i = 1; i <= totalPages; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${currentPage === i ? 'active' : ''}`;
            const a = document.createElement('a');
            a.className = 'page-link';
            a.href = '#';
            a.textContent = i.toString();
            a.onclick = (e) => {
                e.preventDefault();
                studentController.changePage(i);
            };
            li.appendChild(a);
            ul.appendChild(li);
        }
        // Botón para ir a la página siguiente
        const nextLi = document.createElement('li');
        nextLi.className = 'page-item';
        const nextLink = document.createElement('a');
        nextLink.className = 'page-link';
        nextLink.href = '#';
        nextLink.setAttribute('aria-label', 'Next');
        nextLink.innerHTML = '<span aria-hidden="true">&raquo;</span>';
        nextLink.onclick = () => {
            if (currentPage < totalPages)
                studentController.changePage(currentPage + 1);
        };
        nextLi.appendChild(nextLink);
        ul.appendChild(nextLi);
        nav.appendChild(ul);
        return nav;
    }
}
