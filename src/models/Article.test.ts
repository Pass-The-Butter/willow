import { createArticle, updateArticle, Article, CreateArticleInput, UpdateArticleInput } from './Article';

describe('Article model', () => {
  describe('createArticle', () => {
    it('should create an article with all required fields', () => {
      const input: CreateArticleInput = {
        title: 'Getting Started with Willow',
        content: 'This is a guide to get started.',
        author: 'John Doe',
      };

      const article = createArticle(input);

      expect(article.id).toBeDefined();
      expect(article.title).toBe(input.title);
      expect(article.content).toBe(input.content);
      expect(article.author).toBe(input.author);
      expect(article.tags).toEqual([]);
      expect(article.createdAt).toBeInstanceOf(Date);
      expect(article.updatedAt).toBeInstanceOf(Date);
    });

    it('should create an article with tags', () => {
      const input: CreateArticleInput = {
        title: 'TypeScript Best Practices',
        content: 'Here are some TypeScript best practices.',
        author: 'Jane Smith',
        tags: ['typescript', 'best-practices', 'coding'],
      };

      const article = createArticle(input);

      expect(article.tags).toEqual(['typescript', 'best-practices', 'coding']);
    });

    it('should generate unique IDs for different articles', () => {
      const input: CreateArticleInput = {
        title: 'Test Article',
        content: 'Test content',
        author: 'Test Author',
      };

      const article1 = createArticle(input);
      const article2 = createArticle(input);

      expect(article1.id).not.toBe(article2.id);
    });
  });

  describe('updateArticle', () => {
    it('should update title and keep other fields', () => {
      const article: Article = {
        id: '123',
        title: 'Original Title',
        content: 'Original content',
        author: 'Author',
        tags: ['tag1'],
        createdAt: new Date('2024-01-01'),
        updatedAt: new Date('2024-01-01'),
      };

      const input: UpdateArticleInput = {
        title: 'Updated Title',
      };

      const updated = updateArticle(article, input);

      expect(updated.title).toBe('Updated Title');
      expect(updated.content).toBe('Original content');
      expect(updated.author).toBe('Author');
      expect(updated.tags).toEqual(['tag1']);
      expect(updated.createdAt).toEqual(article.createdAt);
      expect(updated.updatedAt.getTime()).toBeGreaterThan(article.updatedAt.getTime());
    });

    it('should update content', () => {
      const article: Article = {
        id: '123',
        title: 'Title',
        content: 'Original content',
        author: 'Author',
        tags: [],
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      const input: UpdateArticleInput = {
        content: 'New content here',
      };

      const updated = updateArticle(article, input);

      expect(updated.content).toBe('New content here');
      expect(updated.title).toBe('Title');
    });

    it('should update tags', () => {
      const article: Article = {
        id: '123',
        title: 'Title',
        content: 'Content',
        author: 'Author',
        tags: ['old-tag'],
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      const input: UpdateArticleInput = {
        tags: ['new-tag', 'another-tag'],
      };

      const updated = updateArticle(article, input);

      expect(updated.tags).toEqual(['new-tag', 'another-tag']);
    });

    it('should update multiple fields at once', () => {
      const article: Article = {
        id: '123',
        title: 'Original',
        content: 'Original content',
        author: 'Author',
        tags: [],
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      const input: UpdateArticleInput = {
        title: 'New Title',
        content: 'New content',
        tags: ['tag1', 'tag2'],
      };

      const updated = updateArticle(article, input);

      expect(updated.title).toBe('New Title');
      expect(updated.content).toBe('New content');
      expect(updated.tags).toEqual(['tag1', 'tag2']);
    });
  });
});
