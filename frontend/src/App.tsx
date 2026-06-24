import { FileUp, Loader2, Replace, Sparkles } from "lucide-react";
import { useMemo, useState } from "react";

import { DataTable } from "./components/DataTable";
import { StatusMessage } from "./components/StatusMessage";
import { ApiClientError, generateRegex, previewFile, processFile } from "./services/apiClient";
import type { DataRow, FilePreviewResponse, FileProcessResponse, RegexGenerateResponse } from "./types/api";

type AsyncAction = "preview" | "generate" | "replace" | null;

const DEFAULT_NATURAL_LANGUAGE = "Find email addresses in the Email column";
const DEFAULT_REPLACEMENT = "REDACTED";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<FilePreviewResponse | null>(null);
  const [selectedColumn, setSelectedColumn] = useState("");
  const [naturalLanguage, setNaturalLanguage] = useState(DEFAULT_NATURAL_LANGUAGE);
  const [regexResult, setRegexResult] = useState<RegexGenerateResponse | null>(null);
  const [replacement, setReplacement] = useState(DEFAULT_REPLACEMENT);
  const [replaceResult, setReplaceResult] = useState<FileProcessResponse | null>(null);
  const [error, setError] = useState<{ title: string; detail?: string } | null>(null);
  const [activeAction, setActiveAction] = useState<AsyncAction>(null);

  const displayRows = replaceResult?.rows ?? preview?.rows ?? [];
  const displayColumns = replaceResult?.columns ?? preview?.columns ?? [];
  const canGenerate = Boolean(preview && selectedColumn && naturalLanguage.trim());
  const canReplace = Boolean(preview && selectedColumn && regexResult?.regex);

  const sampleValues = useMemo(() => {
    if (!preview || !selectedColumn) {
      return [];
    }

    return preview.rows
      .map((row) => row[selectedColumn])
      .filter((value): value is NonNullable<DataRow[string]> => value !== null && value !== undefined)
      .map(String)
      .slice(0, 5);
  }, [preview, selectedColumn]);

  async function handlePreview() {
    if (!file) {
      setError({ title: "Select a file first." });
      return;
    }

    await runAction("preview", async () => {
      const result = await previewFile(file);
      setPreview(result);
      setSelectedColumn(result.columns.includes("Email") ? "Email" : result.columns[0] ?? "");
      setRegexResult(null);
      setReplaceResult(null);
    });
  }

  async function handleGenerate() {
    await runAction("generate", async () => {
      const result = await generateRegex({
        naturalLanguage,
        targetColumn: selectedColumn,
        sampleValues,
      });
      setRegexResult(result);
      setReplaceResult(null);
    });
  }

  async function handleReplace() {
    if (!file || !preview || !regexResult) {
      return;
    }

    await runAction("replace", async () => {
      const result = await processFile({
        file,
        targetColumn: selectedColumn,
        regex: regexResult.regex,
        replacement,
      });
      setReplaceResult(result);
    });
  }

  async function runAction(action: AsyncAction, callback: () => Promise<void>) {
    setError(null);
    setActiveAction(action);
    try {
      await callback();
    } catch (caught) {
      setError(formatError(caught));
    } finally {
      setActiveAction(null);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace-header">
        <div>
          <p className="eyebrow">Regex Pattern Replacement</p>
          <h1>Data Pattern Workbench</h1>
        </div>
        <div className="endpoint-pill">Backend API: {import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api"}</div>
      </section>

      {error ? <StatusMessage tone="error" title={error.title} detail={error.detail} /> : null}

      <section className="workspace-grid">
        <aside className="control-panel">
          <div className="control-block">
            <label htmlFor="file">File</label>
            <input
              id="file"
              type="file"
              accept=".csv,.xlsx"
              onChange={(event) => {
                setFile(event.target.files?.[0] ?? null);
                setPreview(null);
                setRegexResult(null);
                setReplaceResult(null);
                setError(null);
              }}
            />
            <button className="primary-button" type="button" onClick={handlePreview} disabled={!file || activeAction !== null}>
              {activeAction === "preview" ? <Loader2 className="spin" size={18} /> : <FileUp size={18} />}
              Preview data
            </button>
          </div>

          <div className="control-block">
            <label htmlFor="column">Target column</label>
            <select
              id="column"
              value={selectedColumn}
              disabled={!preview || activeAction !== null}
              onChange={(event) => {
                setSelectedColumn(event.target.value);
                setRegexResult(null);
                setReplaceResult(null);
              }}
            >
              {preview?.columns.map((column) => (
                <option key={column} value={column}>
                  {column}
                </option>
              ))}
            </select>
          </div>

          <div className="control-block">
            <label htmlFor="natural-language">Natural language</label>
            <textarea
              id="natural-language"
              value={naturalLanguage}
              disabled={activeAction !== null}
              onChange={(event) => setNaturalLanguage(event.target.value)}
              rows={4}
            />
            <button className="secondary-button" type="button" onClick={handleGenerate} disabled={!canGenerate || activeAction !== null}>
              {activeAction === "generate" ? <Loader2 className="spin" size={18} /> : <Sparkles size={18} />}
              Generate regex
            </button>
          </div>

          <div className="control-block">
            <label htmlFor="regex">Regex</label>
            <input id="regex" value={regexResult?.regex ?? ""} readOnly />
            {regexResult ? (
              <p className="field-note">
                {regexResult.explanation} Provider: {regexResult.provider}.
              </p>
            ) : null}
          </div>

          <div className="control-block">
            <label htmlFor="replacement">Replacement</label>
            <input
              id="replacement"
              value={replacement}
              disabled={activeAction !== null}
              onChange={(event) => setReplacement(event.target.value)}
            />
            <button className="primary-button" type="button" onClick={handleReplace} disabled={!canReplace || activeAction !== null}>
              {activeAction === "replace" ? <Loader2 className="spin" size={18} /> : <Replace size={18} />}
              Replace matches
            </button>
          </div>
        </aside>

        <section className="data-panel">
          <div className="data-toolbar">
            <div>
              <h2>{replaceResult ? "Processed data" : "Preview data"}</h2>
              <p>
                {preview
                  ? `${preview.filename} | ${displayRows.length} shown of ${replaceResult?.row_count ?? preview.row_count} rows`
                  : "No file loaded"}
              </p>
            </div>
            {replaceResult ? (
              <div className="stats">
                <span>{replaceResult.replacement_count} replacements</span>
                <span>{replaceResult.affected_row_count} rows affected</span>
              </div>
            ) : null}
          </div>

          {replaceResult ? (
            <StatusMessage
              tone="success"
              title="Replacement complete"
              detail={`${replaceResult.replacement_count} matches replaced across ${replaceResult.affected_row_count} rows.`}
            />
          ) : null}

          <DataTable columns={displayColumns} rows={displayRows} emptyLabel="Upload a CSV or Excel file." />
        </section>
      </section>
    </main>
  );
}

function formatError(caught: unknown) {
  if (caught instanceof ApiClientError) {
    return { title: getErrorTitle(caught.code), detail: caught.message };
  }
  if (caught instanceof Error) {
    return { title: "UNEXPECTED_ERROR", detail: caught.message };
  }
  return { title: "UNEXPECTED_ERROR" };
}

function getErrorTitle(code: string) {
  const titles: Record<string, string> = {
    EMPTY_DESCRIPTION: "Enter a pattern description",
    FILE_PARSE_ERROR: "File could not be parsed",
    FILE_TOO_LARGE: "File is too large",
    INVALID_FILE_TYPE: "Unsupported file type",
    INVALID_REGEX: "Generated regex is invalid",
    INVALID_REQUEST_BODY: "Request data is invalid",
    INVALID_RESPONSE: "Backend response is invalid",
    LLM_AUTHENTICATION_FAILED: "OpenAI authentication failed",
    LLM_CONFIGURATION_ERROR: "LLM configuration is incomplete",
    LLM_CONNECTION_FAILED: "OpenAI is unavailable",
    LLM_GENERATION_FAILED: "Regex could not be generated",
    LLM_INCOMPLETE_RESPONSE: "Model response was incomplete",
    LLM_INVALID_RESPONSE: "Model response was invalid",
    LLM_RATE_LIMITED: "OpenAI rate limit reached",
    LLM_REFUSED: "Model declined the request",
    LLM_TIMEOUT: "OpenAI request timed out",
    NETWORK_ERROR: "Backend is unavailable",
    REQUEST_TIMEOUT: "Request timed out",
    REQUEST_VALIDATION_ERROR: "Check the submitted values",
    TARGET_COLUMN_NOT_FOUND: "Target column was not found",
    TOO_MANY_ROWS: "File has too many rows",
  };

  return titles[code] ?? code;
}
