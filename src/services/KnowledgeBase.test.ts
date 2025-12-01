import { KnowledgeBase } from './KnowledgeBase';

describe('KnowledgeBase', () => {
  let kb: KnowledgeBase;

  beforeEach(() => {
    kb = new KnowledgeBase();
  });

  describe('addArticle', () => {
    it('should add an article and return it', () => {
      const article = kb.addArticle({
        title: 'Test Article',
        content: 'Test content',
        author: 'Test Author',
      });

      expect(article.id).toBeDefined();
      expect(article.title).toBe('Test Article');
    });

    it('should add article with tags', () => {
      const article = kb.addArticle({
        title: 'Tagged Article',
        content: 'Content with tags',
        author: 'Author',
        tags: ['tag1', 'tag2'],
      });

      expect(article.tags).toEqual(['tag1', 'tag2']);
    });
  });

  describe('getArticle', () => {
    it('should retrieve an article by id', () => {
      const added = kb.addArticle({
        title: 'My Article',
        content: 'Content',
        author: 'Author',
      });

      const retrieved = kb.getArticle(added.id);

      expect(retrieved).toEqual(added);
    });

    it('should return undefined for non-existent id', () => {
      const retrieved = kb.getArticle('non-existent-id');

      expect(retrieved).toBeUndefined();
    });
  });

  describe('getAllArticles', () => {
    it('should return empty array when no articles', () => {
      const articles = kb.getAllArticles();

      expect(articles).toEqual([]);
    });

    it('should return all articles', () => {
      kb.addArticle({ title: 'Article 1', content: 'Content 1', author: 'Author' });
      kb.addArticle({ title: 'Article 2', content: 'Content 2', author: 'Author' });
      kb.addArticle({ title: 'Article 3', content: 'Content 3', author: 'Author' });

      const articles = kb.getAllArticles();

      expect(articles.length).toBe(3);
    });
  });

  describe('updateArticle', () => {
    it('should update an existing article', () => {
      const article = kb.addArticle({
        title: 'Original Title',
        content: 'Original content',
        author: 'Author',
      });

      const updated = kb.updateArticle(article.id, {
        title: 'New Title',
      });

      expect(updated).toBeDefined();
      expect(updated?.title).toBe('New Title');
      expect(updated?.content).toBe('Original content');
    });

    it('should return undefined for non-existent article', () => {
      const result = kb.updateArticle('fake-id', { title: 'New Title' });

      expect(result).toBeUndefined();
    });
  });

  describe('deleteArticle', () => {
    it('should delete an existing article', () => {
      const article = kb.addArticle({
        title: 'To Delete',
        content: 'Content',
        author: 'Author',
      });

      const deleted = kb.deleteArticle(article.id);

      expect(deleted).toBe(true);
      expect(kb.getArticle(article.id)).toBeUndefined();
    });

    it('should return false for non-existent article', () => {
      const deleted = kb.deleteArticle('fake-id');

      expect(deleted).toBe(false);
    });
  });

  describe('searchArticles', () => {
    beforeEach(() => {
      kb.addArticle({
        title: 'TypeScript Guide',
        content: 'Learn TypeScript basics',
        author: 'Dev',
      });
      kb.addArticle({
        title: 'JavaScript Tutorial',
        content: 'JavaScript fundamentals explained',
        author: 'Dev',
      });
      kb.addArticle({
        title: 'Python for Data Science',
        content: 'Using Python for data analysis',
        author: 'Data Scientist',
      });
    });

    it('should find articles by title', () => {
      const results = kb.searchArticles('TypeScript');

      expect(results.length).toBe(1);
      expect(results[0].title).toBe('TypeScript Guide');
    });

    it('should find articles by content', () => {
      const results = kb.searchArticles('fundamentals');

      expect(results.length).toBe(1);
      expect(results[0].title).toBe('JavaScript Tutorial');
    });

    it('should be case-insensitive', () => {
      const results = kb.searchArticles('python');

      expect(results.length).toBe(1);
      expect(results[0].title).toBe('Python for Data Science');
    });

    it('should return empty array when no matches', () => {
      const results = kb.searchArticles('nonexistent');

      expect(results).toEqual([]);
    });

    it('should return empty array for empty query', () => {
      const results = kb.searchArticles('');

      expect(results).toEqual([]);
    });

    it('should return empty array for whitespace-only query', () => {
      const results = kb.searchArticles('   ');

      expect(results).toEqual([]);
    });

    it('should trim query before searching', () => {
      const results = kb.searchArticles('  TypeScript  ');

      expect(results.length).toBe(1);
      expect(results[0].title).toBe('TypeScript Guide');
    });
  });

  describe('getArticlesByTag', () => {
    beforeEach(() => {
      kb.addArticle({
        title: 'Article 1',
        content: 'Content',
        author: 'Author',
        tags: ['javascript', 'frontend'],
      });
      kb.addArticle({
        title: 'Article 2',
        content: 'Content',
        author: 'Author',
        tags: ['javascript', 'backend'],
      });
      kb.addArticle({
        title: 'Article 3',
        content: 'Content',
        author: 'Author',
        tags: ['python', 'backend'],
      });
    });

    it('should find articles by tag', () => {
      const results = kb.getArticlesByTag('javascript');

      expect(results.length).toBe(2);
    });

    it('should be case-insensitive', () => {
      const results = kb.getArticlesByTag('BACKEND');

      expect(results.length).toBe(2);
    });

    it('should return empty array for non-existent tag', () => {
      const results = kb.getArticlesByTag('rust');

      expect(results).toEqual([]);
    });
  });

  describe('getAllTags', () => {
    it('should return empty array when no articles', () => {
      const tags = kb.getAllTags();

      expect(tags).toEqual([]);
    });

    it('should return all unique tags', () => {
      kb.addArticle({
        title: 'Article 1',
        content: 'Content',
        author: 'Author',
        tags: ['tag1', 'tag2'],
      });
      kb.addArticle({
        title: 'Article 2',
        content: 'Content',
        author: 'Author',
        tags: ['tag2', 'tag3'],
      });

      const tags = kb.getAllTags();

      expect(tags).toHaveLength(3);
      expect(tags).toContain('tag1');
      expect(tags).toContain('tag2');
      expect(tags).toContain('tag3');
    });
  });

  describe('getArticleCount', () => {
    it('should return 0 when empty', () => {
      expect(kb.getArticleCount()).toBe(0);
    });

    it('should return correct count', () => {
      kb.addArticle({ title: 'A1', content: 'C1', author: 'Auth' });
      kb.addArticle({ title: 'A2', content: 'C2', author: 'Auth' });

      expect(kb.getArticleCount()).toBe(2);
    });
  });

  describe('clear', () => {
    it('should remove all articles', () => {
      kb.addArticle({ title: 'A1', content: 'C1', author: 'Auth' });
      kb.addArticle({ title: 'A2', content: 'C2', author: 'Auth' });

      kb.clear();

      expect(kb.getArticleCount()).toBe(0);
      expect(kb.getAllArticles()).toEqual([]);
    });
  });
});
