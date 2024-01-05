import { StudentDetailsRenderer } from '../../renderer/StudentDetailsRenderer.js';
// Describes test suite for StudentDetailsRenderer
describe('StudentDetailsRenderer', () => {
    let renderer;
    beforeEach(() => {
        // Initialize the StudentDetailsRenderer before each test
        renderer = new StudentDetailsRenderer();
    });
    // Test to ensure student details are rendered correctly
    test('should render student details correctly', () => {
        // Define a mock student object
        const student = {
            id: 1,
            name: 'Juan',
            lastname: 'Perez',
            phone: '123456789',
            email: 'juan.perez@example.com'
        };
        // Render student details using the renderer
        const renderedElement = renderer.render(student);
        // Assert that the rendered element has correct class and contains expected content
        expect(renderedElement.className).toBe('container mt-3');
        expect(renderedElement.innerHTML).toContain('<th scope="row" class="table-active">ID</th>');
        expect(renderedElement.innerHTML).toContain('<td>1</td>');
        expect(renderedElement.innerHTML).toContain('<td>Juan</td>');
        expect(renderedElement.innerHTML).toContain('<td>Perez</td>');
        expect(renderedElement.innerHTML).toContain('<td>123456789</td>');
        expect(renderedElement.innerHTML).toContain('<td>juan.perez@example.com</td>');
    });
});
