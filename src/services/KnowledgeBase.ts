import { Article, CreateArticleInput, UpdateArticleInput, createArticle, updateArticle } from '../models';

/**
 * KnowledgeBase service - the core of the Company Brain
 * Manages knowledge articles, providing CRUD operations and search functionality
 */
export class KnowledgeBase {
  private articles: Map<string, Article> = new Map();

  /**
   * Add a new article to the knowledge base
   */
  addArticle(input: CreateArticleInput): Article {
    const article = createArticle(input);
    this.articles.set(article.id, article);
    return article;
  }

  /**
   * Get an article by its ID
   */
  getArticle(id: string): Article | undefined {
    return this.articles.get(id);
  }

  /**
   * Get all articles in the knowledge base
   */
  getAllArticles(): Article[] {
    return Array.from(this.articles.values());
  }

  /**
   * Update an existing article
   */
  updateArticle(id: string, input: UpdateArticleInput): Article | undefined {
    const article = this.articles.get(id);
    if (!article) {
      return undefined;
    }
    const updated = updateArticle(article, input);
    this.articles.set(id, updated);
    return updated;
  }

  /**
   * Delete an article by its ID
   */
  deleteArticle(id: string): boolean {
    return this.articles.delete(id);
  }

  /**
   * Search articles by title or content
   */
  searchArticles(query: string): Article[] {
    // Validate query is a non-empty string
    if (!query || typeof query !== 'string' || query.trim().length === 0) {
      return [];
    }
    
    const lowerQuery = query.trim().toLowerCase();
    return this.getAllArticles().filter(
      (article) =>
        article.title.toLowerCase().includes(lowerQuery) ||
        article.content.toLowerCase().includes(lowerQuery)
    );
  }

  /**
   * Find articles by tag
   */
  getArticlesByTag(tag: string): Article[] {
    const lowerTag = tag.toLowerCase();
    return this.getAllArticles().filter((article) =>
      article.tags.some((t) => t.toLowerCase() === lowerTag)
    );
  }

  /**
   * Get all unique tags in the knowledge base
   */
  getAllTags(): string[] {
    const tags = new Set<string>();
    this.getAllArticles().forEach((article) => {
      article.tags.forEach((tag) => tags.add(tag));
    });
    return Array.from(tags);
  }

  /**
   * Get the total count of articles
   */
  getArticleCount(): number {
    return this.articles.size;
  }

  /**
   * Clear all articles from the knowledge base
   */
  clear(): void {
    this.articles.clear();
  }
}
