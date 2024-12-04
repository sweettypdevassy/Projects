const request = require('supertest');
const app = require('./app');

let server; // Store the server instance

beforeAll(() => {
    server = app.listen(); // Start the server
});

afterAll((done) => {
    server.close(done); // Close the server after all tests
});

test('GET /', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
});
