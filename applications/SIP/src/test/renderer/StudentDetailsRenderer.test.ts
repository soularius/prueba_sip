import { StudentDetailsRenderer } from '../../renderer/StudentDetailsRenderer';
import { Student } from '../../models/Student';

describe('StudentDetailsRenderer', () => {
  let renderer: StudentDetailsRenderer;

  beforeEach(() => {
    renderer = new StudentDetailsRenderer();
  });

  test('should render student details correctly', () => {
    const student: Student = {
      id: 1,
      name: 'Juan',
      lastname: 'Perez',
      phone: '123456789',
      email: 'juan.perez@example.com'
    };
  
    const renderedElement = renderer.render(student);
    
    expect(renderedElement.className).toBe('container mt-3');
    expect(renderedElement.innerHTML).toContain('<th scope="row" class="table-active">ID</th>');
    expect(renderedElement.innerHTML).toContain('<td>1</td>');
    expect(renderedElement.innerHTML).toContain('<td>Juan</td>');
    expect(renderedElement.innerHTML).toContain('<td>Perez</td>');
    expect(renderedElement.innerHTML).toContain('<td>123456789</td>');
    expect(renderedElement.innerHTML).toContain('<td>juan.perez@example.com</td>');
  });
});
