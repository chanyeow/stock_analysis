export interface LogFileInfo {
  name: string;
  size: number;
  modifiedAt: string;
}

export interface LogListResponse {
  files: LogFileInfo[];
}

export interface LogContentResponse {
  name: string;
  lines: string[];
  readLines: number;
}
