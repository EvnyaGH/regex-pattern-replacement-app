# API Reference

The Django Ninja API exposes health, file preview, full-file processing, regex
generation, and lower-level row replacement endpoints.

Base URLs:

```text
Local:      http://127.0.0.1:8000/api
Production: https://regex-pattern-replacement-api.onrender.com/api
```

Interactive production documentation:

https://regex-pattern-replacement-api.onrender.com/api/docs

## Common Error Shape

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message.",
    "details": {}
  }
}
```

Missing fields and invalid field types return HTTP 422 with `REQUEST_VALIDATION_ERROR`. Malformed JSON returns HTTP 400 with `INVALID_REQUEST_BODY`. Both use the common error shape.

## GET /health

Checks whether the backend is running.

### Success Response

```json
{
  "status": "ok"
}
```

### Validation

- Should return HTTP 200 when the backend is healthy.

## POST /files/preview

Uploads a CSV or Excel file and returns preview data.

### Request

Content type:

```text
multipart/form-data
```

Fields:

| Field | Type | Required | Description |
|---|---|---|---|
| file | File | Yes | `.csv` or `.xlsx` file |
| preview_limit | Integer | No | Number of rows to preview, default 50 |

Constraints:

- Supported extensions: `.csv`, `.xlsx`.
- Default preview limit: 50 rows.
- Maximum preview limit: configured by `MAX_PREVIEW_ROWS`, default 200.
- Maximum upload size: configured by `MAX_UPLOAD_BYTES`, default 5 MB.

### Success Response

```json
{
  "filename": "sample.csv",
  "columns": ["ID", "Name", "Email"],
  "rows": [
    {"ID": 1, "Name": "John Doe", "Email": "john.doe@example.com"},
    {"ID": 2, "Name": "Jane Smith", "Email": "jane_smith@domain.com"}
  ],
  "row_count": 3,
  "preview_limit": 50
}
```

### Error Cases

- `INVALID_FILE_TYPE`: uploaded file is not CSV or Excel.
- `EMPTY_FILE`: file has no readable rows.
- `FILE_PARSE_ERROR`: file cannot be parsed.
- `FILE_TOO_LARGE`: uploaded file exceeds configured limit.
- `INVALID_PREVIEW_LIMIT`: preview limit is below 1 or above the configured maximum.

## POST /files/process

Re-uploads the original CSV or Excel file, applies regex replacement to every row, and returns a limited processed preview plus full-file statistics.

### Request

Content type:

```text
multipart/form-data
```

| Field | Type | Required | Description |
|---|---|---|---|
| file | File | Yes | Original `.csv` or `.xlsx` file |
| target_column | String | Yes | Column where replacement is applied |
| regex | String | Yes | Compilable Python regex |
| replacement | String | No | Replacement text; empty deletes matches |
| preview_limit | Integer | No | Processed rows returned for display, default 50 |

The complete file is processed. `preview_limit` limits only the response rows, not the rows included in replacement statistics.

### Success Response

```json
{
  "filename": "sample.csv",
  "columns": ["ID", "Name", "Email"],
  "rows": [
    {"ID": 1, "Name": "John Doe", "Email": "REDACTED"}
  ],
  "row_count": 60,
  "preview_limit": 50,
  "replacement_count": 60,
  "affected_row_count": 60
}
```

### Error Cases

- File validation errors from `/files/preview`.
- `MISSING_TARGET_COLUMN`: target column is empty.
- `TARGET_COLUMN_NOT_FOUND`: target column is not present in the file.
- `INVALID_REGEX`: regex is empty or cannot be compiled.
- `NO_ROWS`: the uploaded file has no data rows.

## POST /regex/generate

Generates a regex pattern from natural language.

Provider behavior:

- The mock LLM only supports email address pattern generation.
- Unknown descriptions return `LLM_GENERATION_FAILED`.
- The OpenAI provider uses strict Structured Outputs and can handle broader pattern descriptions.
- Provider selection is controlled by `LLM_PROVIDER`.

### Request

```json
{
  "natural_language": "Find email addresses in the Email column",
  "target_column": "Email",
  "sample_values": [
    "john.doe@example.com",
    "jane_smith@domain.com",
    "alice.brown@website.org"
  ]
}
```

### Success Response

```json
{
  "regex": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,7}\\b",
  "explanation": "Matches common email addresses using local-part, domain, and TLD groups.",
  "provider": "mock"
}
```

### Error Cases

- `EMPTY_DESCRIPTION`: natural language input is empty.
- `MISSING_TARGET_COLUMN`: target column is missing.
- `LLM_GENERATION_FAILED`: LLM provider failed to generate a regex.
- `LLM_CONFIGURATION_ERROR`: provider configuration or API key is missing.
- `LLM_AUTHENTICATION_FAILED`: credentials or model access failed.
- `LLM_RATE_LIMITED`: OpenAI rate limit was reached.
- `LLM_TIMEOUT`: OpenAI request timed out.
- `LLM_CONNECTION_FAILED`: backend could not connect to OpenAI.
- `LLM_REFUSED`: model declined the request.
- `LLM_INCOMPLETE_RESPONSE`: model output was incomplete.
- `LLM_INVALID_RESPONSE`: provider output did not satisfy the expected contract.
- `INVALID_GENERATED_REGEX`: generated regex cannot be compiled.

## POST /regex/replace

Applies a regex replacement to rows supplied as JSON. This remains the lower-level row transformation endpoint; the frontend uses `/files/process` so replacement covers the complete uploaded file.

Replacement behavior:

- Regex is applied only to `target_column`.
- Non-target columns are preserved.
- `replacement_count` counts total matches replaced.
- `affected_row_count` counts rows where at least one match was replaced.
- No-match cases return HTTP 200 with zero counts.

### Request

```json
{
  "columns": ["ID", "Name", "Email"],
  "rows": [
    {"ID": 1, "Name": "John Doe", "Email": "john.doe@example.com"},
    {"ID": 2, "Name": "Jane Smith", "Email": "jane_smith@domain.com"},
    {"ID": 3, "Name": "Alice Brown", "Email": "alice.brown@website.org"}
  ],
  "target_column": "Email",
  "regex": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,7}\\b",
  "replacement": "REDACTED"
}
```

### Success Response

```json
{
  "columns": ["ID", "Name", "Email"],
  "rows": [
    {"ID": 1, "Name": "John Doe", "Email": "REDACTED"},
    {"ID": 2, "Name": "Jane Smith", "Email": "REDACTED"},
    {"ID": 3, "Name": "Alice Brown", "Email": "REDACTED"}
  ],
  "replacement_count": 3,
  "affected_row_count": 3
}
```

### Error Cases

- `MISSING_TARGET_COLUMN`: target column is missing.
- `TARGET_COLUMN_NOT_FOUND`: target column does not exist in uploaded data.
- `INVALID_REGEX`: regex is empty or cannot be compiled.
- `NO_ROWS`: request contains no rows.

### Non-Error Edge Case

No matches found should return HTTP 200 with:

```json
{
  "replacement_count": 0,
  "affected_row_count": 0
}
```

## Planned API

## POST /files/export

Processed-file export is not implemented. CSV export is the next planned
addition; Excel export remains optional.
