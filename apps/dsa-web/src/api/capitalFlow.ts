import apiClient from './index';
import { toCamelCase } from './utils';

export interface CapitalFlowItem {
  code: string;
  name: string;
  flow: number;
}

export interface CapitalFlowResponse {
  category: string;
  period: string;
  total: number;
  data: CapitalFlowItem[];
}

export interface CapitalFlowTableItem {
  code: string;
  name: string;
  flow: number;
  price: number | null;
  changePct: number | null;
  companyCount: number | null;
  leadStockName: string;
  leadStockCode: string;
  mainFlow: number | null;
  mainRatio: number | null;
  superLargeFlow: number | null;
  largeFlow: number | null;
  mediumFlow: number | null;
  smallFlow: number | null;
  superLargeRatio: number | null;
  largeRatio: number | null;
  mediumRatio: number | null;
  smallRatio: number | null;
}

export interface CapitalFlowTableResponse {
  category: string;
  period: string;
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
  data: CapitalFlowTableItem[];
}

export const capitalFlowApi = {
  /**
   * Get chart data for industry/concept sectors from knowledge base (markdown files).
   */
  getData: async (
    category: 'industry' | 'concept' = 'industry',
    _period: string = 'today',
    _forceRefresh: boolean = false,
  ): Promise<CapitalFlowResponse> => {
    const response = await apiClient.get<Record<string, unknown>>(
      '/api/v1/knowledge/capital-flow/data',
      { params: { category } },
    );
    return toCamelCase<CapitalFlowResponse>(response.data);
  },

  /**
   * Get table data with pagination and richer fields from knowledge base (markdown files).
   */
  getTable: async (
    category: 'industry' | 'concept' = 'industry',
    period: string = 'today',
    page: number = 1,
    pageSize: number = 50,
    _forceRefresh: boolean = false,
  ): Promise<CapitalFlowTableResponse> => {
    const response = await apiClient.get<Record<string, unknown>>(
      '/api/v1/knowledge/capital-flow/table',
      { params: { category, period, page, page_size: pageSize } },
    );
    return toCamelCase<CapitalFlowTableResponse>(response.data);
  },
};
