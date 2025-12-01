import express, { Express, Request, Response } from 'express';
import { KnowledgeBase } from './services';
import { createArticleRoutes } from './routes';

/**
 * Creates and configures the Willow Express application
 */
export function createApp(kb?: KnowledgeBase): Express {
  const app = express();
  const knowledgeBase = kb || new KnowledgeBase();

  // Middleware
  app.use(express.json());

  // Health check
  app.get('/health', (_req: Request, res: Response) => {
    res.json({ status: 'ok', name: 'Willow - the Company Brain' });
  });

  // API info
  app.get('/', (_req: Request, res: Response) => {
    res.json({
      name: 'Willow - the Company Brain',
      version: '1.0.0',
      description: 'A knowledge management system for your organization',
      endpoints: {
        health: 'GET /health',
        articles: {
          list: 'GET /api/articles',
          search: 'GET /api/articles/search?q=query',
          byTag: 'GET /api/articles/tag/:tag',
          tags: 'GET /api/articles/tags',
          get: 'GET /api/articles/:id',
          create: 'POST /api/articles',
          update: 'PUT /api/articles/:id',
          delete: 'DELETE /api/articles/:id',
        },
      },
    });
  });

  // Routes
  app.use('/api/articles', createArticleRoutes(knowledgeBase));

  return app;
}
