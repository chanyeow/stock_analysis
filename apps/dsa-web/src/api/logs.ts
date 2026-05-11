import apiClient from './index';
import { toCamelCase } from './utils';
import type { LogListResponse, LogContentResponse, LogFileInfo } from '../types/logs';

export const logsApi = {
  async getList(): Promise<LogListResponse> {
    const response = await apiClient.get<Record<string, unknown>>('/api/v1/logs');
    const data = toCamelCase<LogListResponse>(response.data);
    return {
      files: (data.files || []).map((file) => toCamelCase<LogFileInfo>(file)),
    };
  },

  async getContent(filename: string, tail = 500): Promise<LogContentResponse> {
    const response = await apiClient.get<Record<string, unknown>>(
      `/api/v1/logs/${encodeURIComponent(filename)}`,
      {
        params: { tail },
      },
    );
    return toCamelCase<LogContentResponse>(response.data);
  },
};
