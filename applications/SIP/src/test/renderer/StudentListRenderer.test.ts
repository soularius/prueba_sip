import { StudentListRenderer } from '../../renderer/StudentListRenderer';
import { StudentController } from '../../controller/StudentController';
import { Student } from '../../models/Student';
import '@testing-library/jest-dom';

// Describes test suite for StudentListRenderer
describe('StudentListRenderer', () => {
  let renderer: StudentListRenderer;
  let mockController: jest.Mocked<StudentController>;

  beforeEach(() => {
    // Initialize mock controller and the StudentListRenderer before each test
    mockController = new StudentController() as jest.Mocked<StudentController>;
    mockController.deleteStudent = jest.fn();
    renderer = new StudentListRenderer(mockController);
    global.confirm = jest.fn().mockReturnValue(true);
  });

  // Test to ensure a table with student data is rendered correctly
  test('should render a table with student data', () => {
    // Define mock students data
    const students: Student[] = [
      { id: 1, name: 'Juan', lastname: 'Perez', phone: '123456789', email: 'juan@example.com' },
      { id: 2, name: 'Mary', lastname: 'Mart', phone: '5656456456', email: 'mary@example.com' },
      //... other students ...
    ];
  
    // Render student list using the renderer
    const divContent = renderer.render(students, 1, 3, mockController);
  
    // Assertions to verify table rendering
    expect(divContent.className).toBe('container');
    expect(divContent.querySelector('table')).not.toBeNull();
    expect(divContent.querySelectorAll('tbody tr').length).toBe(students.length);
    expect(divContent.textContent).toContain('Juan');
    expect(divContent.textContent).toContain('Perez');
    expect(divContent.textContent).toContain('123456789');
    expect(divContent.textContent).toContain('juan@example.com');
  });

  test('should render pagination correctly', () => {
    // Define mock students data
    const students: Student[] = [
      { id: 1, name: 'Juan', lastname: 'Perez', phone: '123456789', email: 'juan@example.com' },
      { id: 2, name: 'Mary', lastname: 'Mart', phone: '5656456456', email: 'mary@example.com' },
      //... other students ...
    ];
  
    // Render student list with pagination using the renderer
    const divContent = renderer.render(students, 1, 3, mockController);
  
    expect(divContent.querySelector('nav')).not.toBeNull();
    expect(divContent.querySelectorAll('ul.pagination li').length).toBeGreaterThan(0);
    // Verificar que los botones de paginación están presentes y tienen el comportamiento esperado
  });
  
  // Assertions to verify pagination rendering
  test('should render action buttons and links for each student', () => {
    window.alert = jest.fn();
    const students: Student[] = [
      { id: 1, name: 'Juan', lastname: 'Perez', phone: '123456789', email: 'juan@example.com' },
      // Add more students if necessary
    ];
  
    const divContent = renderer.render(students, 1, 3, mockController);
  
    // Verify that each row has the action buttons
    students.forEach((student, index) => {
      const tr = divContent.querySelectorAll('tbody tr')[index];
      expect(tr).not.toBeNull();
  
      const viewLink = tr.querySelector(`a[href='/SIP/students/students_view_ts/${student.id}']`);
      const editLink = tr.querySelector(`a[href='/SIP/students/students_edit_ts/${student.id}']`);
      const deleteButton = tr.querySelector('button.btn.btn-danger.btn-sm') as HTMLButtonElement | null;
  
      expect(viewLink).not.toBeNull();
      expect(editLink).not.toBeNull();
      expect(deleteButton).not.toBeNull();
  
      // Simulate delete button click and assert controller behavior
      if (deleteButton) {
        deleteButton.click();
        expect(mockController.deleteStudent).toHaveBeenCalledWith(student.id);
      } else {
        fail('Delete button should not be null');
      }
    });
  });
  
});
