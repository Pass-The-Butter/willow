# Willow

🌳 **Willow - the Company Brain**

A knowledge management system for your organization. Willow helps teams capture, organize, and share company knowledge effectively.

## Features

- **Knowledge Articles**: Create, read, update, and delete knowledge articles
- **Tagging System**: Organize articles with tags for easy categorization
- **Search**: Full-text search across article titles and content
- **RESTful API**: Clean, intuitive API for integrating with other tools

## Quick Start

### Prerequisites

- Node.js 18+ 
- npm 8+

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd willow

# Install dependencies
npm install

# Build the project
npm run build

# Start the server
npm start
```

### Development

```bash
# Run in development mode
npm run dev

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint
```

## API Endpoints

### Health Check
- `GET /health` - Server health status

### Articles
- `GET /api/articles` - List all articles
- `GET /api/articles/:id` - Get a specific article
- `POST /api/articles` - Create a new article
- `PUT /api/articles/:id` - Update an article
- `DELETE /api/articles/:id` - Delete an article

### Search & Tags
- `GET /api/articles/search?q=query` - Search articles
- `GET /api/articles/tag/:tag` - Get articles by tag
- `GET /api/articles/tags` - Get all tags

## API Examples

### Create an Article

```bash
curl -X POST http://localhost:3000/api/articles \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with Willow",
    "content": "This guide will help you get started...",
    "author": "Admin",
    "tags": ["guide", "getting-started"]
  }'
```

### Search Articles

```bash
curl "http://localhost:3000/api/articles/search?q=getting+started"
```

## Project Structure

```
willow/
├── src/
│   ├── models/         # Data models
│   │   └── Article.ts  # Article model and types
│   ├── services/       # Business logic
│   │   └── KnowledgeBase.ts  # Core knowledge management service
│   ├── routes/         # API routes
│   │   └── articles.ts # Article endpoints
│   ├── app.ts          # Express application setup
│   └── index.ts        # Application entry point
├── package.json
├── tsconfig.json
└── README.md
```

## License

MIT
