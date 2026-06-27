import apiClient from './index';
import { toCamelCase } from './utils';

export interface KnowledgeItem {
  code: string;
  name: string;
  category: string;
  changePct: number | null;
}

export interface KnowledgeListResponse {
  total: number;
  data: KnowledgeItem[];
}

export interface KnowledgeMarkdownResponse {
  code: string;
  name: string;
  category: string;
  content: string;
}

export interface CrawlProgressResponse {
  total: number;
  current: number;
  status: string;
  message: string;
  errors: string[];
}

export interface SearchResponse {
  keyword: string;
  total: number;
  data: KnowledgeItem[];
}

export const knowledgeApi = {
  /**
   * Trigger knowledge base crawl.
   */
  triggerCrawl: async (): Promise<CrawlProgressResponse> => {
    const response = await apiClient.post<Record<string, unknown>>(
      '/api/v1/knowledge/crawl',
    );
    return toCamelCase<CrawlProgressResponse>(response.data);
  },

  /**
   * Get crawl progress.
   */
  getProgress: async (): Promise<CrawlProgressResponse> => {
    const response = await apiClient.get<Record<string, unknown>>(
      '/api/v1/knowledge/progress',
    );
    return toCamelCase<CrawlProgressResponse>(response.data);
  },

  /**
   * Get knowledge base list.
   */
  listItems: async (category?: string): Promise<KnowledgeListResponse> => {
    const response = await apiClient.get<Record<string, unknown>>(
      '/api/v1/knowledge/list',
      { params: { category } },
    );
    return toCamelCase<KnowledgeListResponse>(response.data);
  },

  /**
   * Get markdown content for a knowledge item.
   */
  getMarkdown: async (category: string, code: string): Promise<KnowledgeMarkdownResponse> => {
    const response = await apiClient.get<Record<string, unknown>>(
      `/api/v1/knowledge/markdown/${category}/${code}`,
    );
    return toCamelCase<KnowledgeMarkdownResponse>(response.data);
  },

  /**
   * Search knowledge base.
   */
  search: async (keyword: string): Promise<SearchResponse> => {
    const response = await apiClient.get<Record<string, unknown>>(
      '/api/v1/knowledge/search',
      { params: { keyword } },
    );
    return toCamelCase<SearchResponse>(response.data);
  },
};
