import request from 'supertest';
import { createApp } from './app';
import { KnowledgeBase } from './services';

describe('Willow API', () => {
  let app: ReturnType<typeof createApp>;
  let kb: KnowledgeBase;

  beforeEach(() => {
    kb = new KnowledgeBase();
    app = createApp(kb);
  });

  describe('GET /', () => {
    it('should return API info', async () => {
      const res = await request(app).get('/');

      expect(res.status).toBe(200);
      expect(res.body.name).toBe('Willow - the Company Brain');
      expect(res.body.version).toBe('1.0.0');
      expect(res.body.endpoints).toBeDefined();
    });
  });

  describe('GET /health', () => {
    it('should return health status', async () => {
      const res = await request(app).get('/health');

      expect(res.status).toBe(200);
      expect(res.body.status).toBe('ok');
    });
  });

  describe('Articles API', () => {
    describe('GET /api/articles', () => {
      it('should return empty array when no articles', async () => {
        const res = await request(app).get('/api/articles');

        expect(res.status).toBe(200);
        expect(res.body.articles).toEqual([]);
        expect(res.body.count).toBe(0);
      });

      it('should return all articles', async () => {
        kb.addArticle({ title: 'A1', content: 'C1', author: 'Auth' });
        kb.addArticle({ title: 'A2', content: 'C2', author: 'Auth' });

        const res = await request(app).get('/api/articles');

        expect(res.status).toBe(200);
        expect(res.body.articles.length).toBe(2);
        expect(res.body.count).toBe(2);
      });
    });

    describe('POST /api/articles', () => {
      it('should create a new article', async () => {
        const res = await request(app)
          .post('/api/articles')
          .send({
            title: 'New Article',
            content: 'Article content',
            author: 'Test Author',
          });

        expect(res.status).toBe(201);
        expect(res.body.id).toBeDefined();
        expect(res.body.title).toBe('New Article');
      });

      it('should return 400 when missing required fields', async () => {
        const res = await request(app)
          .post('/api/articles')
          .send({
            title: 'Only Title',
          });

        expect(res.status).toBe(400);
        expect(res.body.error).toBeDefined();
      });

      it('should create article with tags', async () => {
        const res = await request(app)
          .post('/api/articles')
          .send({
            title: 'Tagged Article',
            content: 'Content',
            author: 'Author',
            tags: ['tag1', 'tag2'],
          });

        expect(res.status).toBe(201);
        expect(res.body.tags).toEqual(['tag1', 'tag2']);
      });

      it('should return 400 when title is empty string', async () => {
        const res = await request(app)
          .post('/api/articles')
          .send({
            title: '   ',
            content: 'Content',
            author: 'Author',
          });

        expect(res.status).toBe(400);
        expect(res.body.error).toBeDefined();
      });

      it('should return 400 when tags is not an array of strings', async () => {
        const res = await request(app)
          .post('/api/articles')
          .send({
            title: 'Title',
            content: 'Content',
            author: 'Author',
            tags: 'not-an-array',
          });

        expect(res.status).toBe(400);
        expect(res.body.error).toContain('Tags must be an array of strings');
      });

      it('should trim whitespace from input fields', async () => {
        const res = await request(app)
          .post('/api/articles')
          .send({
            title: '  Trimmed Title  ',
            content: '  Trimmed Content  ',
            author: '  Trimmed Author  ',
          });

        expect(res.status).toBe(201);
        expect(res.body.title).toBe('Trimmed Title');
        expect(res.body.content).toBe('Trimmed Content');
        expect(res.body.author).toBe('Trimmed Author');
      });
    });

    describe('GET /api/articles/:id', () => {
      it('should return an article by id', async () => {
        const article = kb.addArticle({
          title: 'Test',
          content: 'Content',
          author: 'Author',
        });

        const res = await request(app).get(`/api/articles/${article.id}`);

        expect(res.status).toBe(200);
        expect(res.body.id).toBe(article.id);
        expect(res.body.title).toBe('Test');
      });

      it('should return 404 for non-existent article', async () => {
        const res = await request(app).get('/api/articles/fake-id');

        expect(res.status).toBe(404);
      });
    });

    describe('PUT /api/articles/:id', () => {
      it('should update an article', async () => {
        const article = kb.addArticle({
          title: 'Original',
          content: 'Content',
          author: 'Author',
        });

        const res = await request(app)
          .put(`/api/articles/${article.id}`)
          .send({
            title: 'Updated Title',
          });

        expect(res.status).toBe(200);
        expect(res.body.title).toBe('Updated Title');
        expect(res.body.content).toBe('Content');
      });

      it('should return 404 for non-existent article', async () => {
        const res = await request(app)
          .put('/api/articles/fake-id')
          .send({ title: 'Updated' });

        expect(res.status).toBe(404);
      });
    });

    describe('DELETE /api/articles/:id', () => {
      it('should delete an article', async () => {
        const article = kb.addArticle({
          title: 'To Delete',
          content: 'Content',
          author: 'Author',
        });

        const res = await request(app).delete(`/api/articles/${article.id}`);

        expect(res.status).toBe(204);
        expect(kb.getArticle(article.id)).toBeUndefined();
      });

      it('should return 404 for non-existent article', async () => {
        const res = await request(app).delete('/api/articles/fake-id');

        expect(res.status).toBe(404);
      });
    });

    describe('GET /api/articles/search', () => {
      beforeEach(() => {
        kb.addArticle({
          title: 'JavaScript Guide',
          content: 'Learn JavaScript',
          author: 'Dev',
        });
        kb.addArticle({
          title: 'Python Tutorial',
          content: 'Python basics',
          author: 'Dev',
        });
      });

      it('should search articles', async () => {
        const res = await request(app).get('/api/articles/search?q=JavaScript');

        expect(res.status).toBe(200);
        expect(res.body.articles.length).toBe(1);
        expect(res.body.articles[0].title).toBe('JavaScript Guide');
      });

      it('should return 400 when query is missing', async () => {
        const res = await request(app).get('/api/articles/search');

        expect(res.status).toBe(400);
      });
    });

    describe('GET /api/articles/tag/:tag', () => {
      it('should get articles by tag', async () => {
        kb.addArticle({
          title: 'Article 1',
          content: 'Content',
          author: 'Author',
          tags: ['typescript'],
        });
        kb.addArticle({
          title: 'Article 2',
          content: 'Content',
          author: 'Author',
          tags: ['javascript'],
        });

        const res = await request(app).get('/api/articles/tag/typescript');

        expect(res.status).toBe(200);
        expect(res.body.articles.length).toBe(1);
        expect(res.body.articles[0].title).toBe('Article 1');
      });
    });

    describe('GET /api/articles/tags', () => {
      it('should get all tags', async () => {
        kb.addArticle({
          title: 'A1',
          content: 'C1',
          author: 'Auth',
          tags: ['tag1', 'tag2'],
        });
        kb.addArticle({
          title: 'A2',
          content: 'C2',
          author: 'Auth',
          tags: ['tag2', 'tag3'],
        });

        const res = await request(app).get('/api/articles/tags');

        expect(res.status).toBe(200);
        expect(res.body.tags.length).toBe(3);
      });
    });
  });
});
