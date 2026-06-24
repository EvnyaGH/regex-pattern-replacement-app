import type {
  ApiErrorPayload,
  FileProcessResponse,
  FilePreviewResponse,
  RegexGenerateResponse,
} from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";
const API_TIMEOUT_MS = readPositiveInteger(import.meta.env.VITE_API_TIMEOUT_MS, 15000);

export class ApiClientError extends Error {
  code: string;
  details?: Record<string, unknown>;

  constructor(code: string, message: string, details?: Record<string, unknown>) {
    super(message);
    this.name = "ApiClientError";
    this.code = code;
    this.details = details;
  }
}

export async function previewFile(file: File, previewLimit = 50): Promise<FilePreviewResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("preview_limit", String(previewLimit));

  return request<FilePreviewResponse>("/files/preview", {
    method: "POST",
    body: formData,
  });
}

export async function generateRegex(params: {
  naturalLanguage: string;
  targetColumn: string;
  sampleValues: string[];
}): Promise<RegexGenerateResponse> {
  return request<RegexGenerateResponse>("/regex/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      natural_language: params.naturalLanguage,
      target_column: params.targetColumn,
      sample_values: params.sampleValues,
    }),
  });
}

export async function processFile(params: {
  file: File;
  targetColumn: string;
  regex: string;
  replacement: string;
  previewLimit?: number;
}): Promise<FileProcessResponse> {
  const formData = new FormData();
  formData.append("file", params.file);
  formData.append("target_column", params.targetColumn);
  formData.append("regex", params.regex);
  formData.append("replacement", params.replacement);
  formData.append("preview_limit", String(params.previewLimit ?? 50));

  return request<FileProcessResponse>("/files/process", {
    method: "POST",
    body: formData,
  });
}

async function request<T>(path: string, init: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), API_TIMEOUT_MS);
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      signal: controller.signal,
    });
  } catch (caught) {
    if (caught instanceof DOMException && caught.name === "AbortError") {
      throw new ApiClientError(
        "REQUEST_TIMEOUT",
        `The backend did not respond within ${API_TIMEOUT_MS} ms.`,
      );
    }
    throw new ApiClientError(
      "NETWORK_ERROR",
      "The backend could not be reached. Confirm that it is running and the API URL is correct.",
    );
  } finally {
    window.clearTimeout(timeoutId);
  }

  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    const apiError = payload as ApiErrorPayload | null;
    if (apiError?.error) {
      throw new ApiClientError(apiError.error.code, apiError.error.message, apiError.error.details);
    }
    throw new ApiClientError("REQUEST_FAILED", `Request failed with status ${response.status}.`);
  }

  if (payload === null) {
    throw new ApiClientError(
      "INVALID_RESPONSE",
      "The backend returned a response that was not valid JSON.",
    );
  }

  return payload as T;
}

function readPositiveInteger(value: string | undefined, fallback: number) {
  const parsed = Number(value);
  return Number.isInteger(parsed) && parsed > 0 ? parsed : fallback;
}
