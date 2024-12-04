const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Hello, CI/CD Pipeline!');
});

if (require.main === module) {
  // Start server only if the app is run directly (not in tests)
  app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

module.exports = app; // Export the app for use in tests
