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
    
    // Validate required fields are present and are non-empty strings
    if (
      !input.title ||
      !input.content ||
      !input.author ||
      typeof input.title !== 'string' ||
      typeof input.content !== 'string' ||
      typeof input.author !== 'string' ||
      input.title.trim().length === 0 ||
      input.content.trim().length === 0 ||
      input.author.trim().length === 0
    ) {
      res.status(400).json({ error: 'Title, content, and author are required and must be non-empty strings' });
      return;
    }

    // Validate tags if provided
    if (input.tags !== undefined) {
      if (!Array.isArray(input.tags) || !input.tags.every((tag) => typeof tag === 'string')) {
        res.status(400).json({ error: 'Tags must be an array of strings' });
        return;
      }
    }
    
    const article = kb.addArticle({
      title: input.title.trim(),
      content: input.content.trim(),
      author: input.author.trim(),
      tags: input.tags?.map((tag) => tag.trim()).filter((tag) => tag.length > 0),
    });
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
