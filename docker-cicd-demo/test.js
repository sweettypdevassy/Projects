const request = require('supertest');
const app = require('./app'); // Import the app

describe('GET /', () => {
  it('should return a 200 status code', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.text).toBe('Hello, CI/CD Pipeline!');
  });
});
