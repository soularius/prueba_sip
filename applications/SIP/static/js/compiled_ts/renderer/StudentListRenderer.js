export class StudentListRenderer {
    constructor(studentController) {
        this.studentController = studentController;
    }
    /**
     * Renders a table of students with actions and pagination.
     *
     * @param {Student[]} students - an array of student objects
     * @param {number} currentPage - the current page number
     * @param {number} totalPages - the total number of pages
     * @param {StudentController} studentController - an instance of the StudentController class
     * @return {HTMLElement} - the rendered table element
     */
    render(students, currentPage, totalPages, studentController) {
        const divContent = document.createElement('div');
        divContent.className = 'container';
        const table = document.createElement('table');
        table.className = 'table'; // Bootstrap class
        // Add table header
        const thead = table.createTHead();
        const row = thead.insertRow();
        const headers = ['ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Acciones'];
        headers.forEach(text => {
            const th = document.createElement('th');
            th.textContent = text;
            th.className = 'text-center';
            row.appendChild(th);
        });
        // Add table rows
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
    /**
     * Handles the click event on the view.
     *
     * @param {number} id - The ID of the item being viewed.
     */
    handleViewClick(id) {
        const container = this.studentController.getContainer();
        console.log(container);
        if (container)
            this.studentController.viewDetails(container, id);
    }
    /**
     * Handle the click event when editing a student.
     *
     * @param {number} id - The ID of the student to edit.
     */
    handleEditClick(id) {
        const container = this.studentController.getContainer();
        if (container)
            this.studentController.editStudent(container, id);
    }
    /**
     * Handles the click event for deleting a student.
     *
     * @param {number} id - The ID of the student to be deleted.
     */
    handleDeleteClick(id) {
        const container = this.studentController.getContainer();
        if (container)
            this.studentController.deleteStudent(id);
    }
    /**
     * Creates a pagination element based on the current page, total number of pages, and student controller.
     *
     * @param {number} currentPage - The current page number.
     * @param {number} totalPages - The total number of pages.
     * @param {StudentController} studentController - The student controller object.
     * @return {HTMLElement} The pagination element.
     */
    createPagination(currentPage, totalPages, studentController) {
        const nav = document.createElement('nav');
        nav.setAttribute('aria-label', 'Page navigation example');
        const ul = document.createElement('ul');
        ul.className = 'pagination';
        // Button to go to the previous page
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
        // Page numbers
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
        // Button to go to the next page
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
