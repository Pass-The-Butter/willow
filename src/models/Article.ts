import { v4 as uuidv4 } from 'uuid';

/**
 * Represents a knowledge article in the Company Brain
 */
export interface Article {
  id: string;
  title: string;
  content: string;
  author: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Input data required to create a new article
 */
export interface CreateArticleInput {
  title: string;
  content: string;
  author: string;
  tags?: string[];
}

/**
 * Input data for updating an existing article
 */
export interface UpdateArticleInput {
  title?: string;
  content?: string;
  tags?: string[];
}

/**
 * Creates a new Article with generated ID and timestamps
 */
export function createArticle(input: CreateArticleInput): Article {
  const now = new Date();
  return {
    id: uuidv4(),
    title: input.title,
    content: input.content,
    author: input.author,
    tags: input.tags || [],
    createdAt: now,
    updatedAt: now,
  };
}

/**
 * Updates an existing article with new data
 */
export function updateArticle(article: Article, input: UpdateArticleInput): Article {
  return {
    ...article,
    title: input.title ?? article.title,
    content: input.content ?? article.content,
    tags: input.tags ?? article.tags,
    updatedAt: new Date(),
  };
}
