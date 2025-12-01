import { createApp } from './app';

const PORT = process.env.PORT || 3000;

const app = createApp();

app.listen(PORT, () => {
  console.log(`
  🌳 Willow - the Company Brain is running!
  
  Server listening on port ${PORT}
  
  API Endpoints:
  - Health: http://localhost:${PORT}/health
  - Articles API: http://localhost:${PORT}/api/articles
  
  Ready to store and share company knowledge!
  `);
});
