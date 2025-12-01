import { Router, Request, Response } from 'express';
import { KnowledgeBase } from '../services';
import { CreateArticleInput, UpdateArticleInput } from '../models';

/**
 * Creates the article routes for the API
 */
export function createArticleRoutes(kb: KnowledgeBase): Router {
  const router = Router();

  // Get all articles
  router.get('/', (_req: Request, res: Response) => {
    const articles = kb.getAllArticles();
    res.json({ articles, count: articles.length });
  });

  // Search articles
  router.get('/search', (req: Request, res: Response) => {
    const query = req.query.q as string;
    if (!query) {
      res.status(400).json({ error: 'Query parameter "q" is required' });
      return;
    }
    const articles = kb.searchArticles(query);
    res.json({ articles, count: articles.length });
  });

  // Get articles by tag
  router.get('/tag/:tag', (req: Request, res: Response) => {
    const articles = kb.getArticlesByTag(req.params.tag);
    res.json({ articles, count: articles.length });
  });

  // Get all tags
  router.get('/tags', (_req: Request, res: Response) => {
    const tags = kb.getAllTags();
    res.json({ tags });
  });

  // Get a specific article
  router.get('/:id', (req: Request, res: Response) => {
    const article = kb.getArticle(req.params.id);
    if (!article) {
      res.status(404).json({ error: 'Article not found' });
      return;
    }
    res.json(article);
  });

  // Create a new article
  router.post('/', (req: Request, res: Response) => {
    const input: CreateArticleInput = req.body;
    
    if (!input.title || !input.content || !input.author) {
      res.status(400).json({ error: 'Title, content, and author are required' });
      return;
    }
    
    const article = kb.addArticle(input);
    res.status(201).json(article);
  });

  // Update an article
  router.put('/:id', (req: Request, res: Response) => {
    const input: UpdateArticleInput = req.body;
    const article = kb.updateArticle(req.params.id, input);
    
    if (!article) {
      res.status(404).json({ error: 'Article not found' });
      return;
    }
    
    res.json(article);
  });

  // Delete an article
  router.delete('/:id', (req: Request, res: Response) => {
    const deleted = kb.deleteArticle(req.params.id);
    
    if (!deleted) {
      res.status(404).json({ error: 'Article not found' });
      return;
    }
    
    res.status(204).send();
  });

  return router;
}
