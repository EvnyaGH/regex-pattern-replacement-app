export type DataValue = string | number | boolean | null;

export type DataRow = Record<string, DataValue>;

export interface ApiErrorPayload {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

export interface FilePreviewResponse {
  filename: string;
  columns: string[];
  rows: DataRow[];
  row_count: number;
  preview_limit: number;
}

export interface RegexGenerateRequest {
  natural_language: string;
  target_column: string;
  sample_values: string[];
}

export interface RegexGenerateResponse {
  regex: string;
  explanation: string;
  provider: string;
}

export interface RegexReplaceRequest {
  columns: string[];
  rows: DataRow[];
  target_column: string;
  regex: string;
  replacement: string;
}

export interface RegexReplaceResponse {
  columns: string[];
  rows: DataRow[];
  replacement_count: number;
  affected_row_count: number;
}

export interface FileProcessResponse extends FilePreviewResponse {
  replacement_count: number;
  affected_row_count: number;
}
