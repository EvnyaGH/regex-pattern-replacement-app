# Architecture

## Overview

Regex Pattern Replacement is a stateless web application with three runtime
components:

```text
React frontend on Vercel
          |
          | HTTPS
          v
Django Ninja API on Render
          |
          | HTTPS, when LLM_PROVIDER=openai
          v
OpenAI Responses API
```

The frontend manages interaction state. The backend owns file validation,
parsing, regex generation, replacement, and API contracts. OpenAI is isolated
behind a provider boundary so local development and tests can use a
deterministic mock.

## Repository Structure

```text
backend/
  api/                    Django Ninja routes and error handlers
  config/                 Django settings, URL, ASGI, and WSGI configuration
  schemas/                Typed request and response models
  scripts/                Quality, production, and live-provider checks
  services/               Parsing, generation, processing, and replacement

frontend/
  scripts/                Windows-compatible Vite launcher
  src/
    components/           Table, status, and error-boundary components
    services/             Typed HTTP client
    types/                API data contracts
    App.tsx               Main workflow and UI state

docs/                     Product and engineering documentation
samples/                  Public sample files
render.yaml               Render Blueprint
```

## Request Flow

### Preview

1. The browser sends a CSV or XLSX file to `/api/files/preview`.
2. The backend validates extension, size, parseability, and preview limit.
3. pandas parses the file and normalizes values for JSON.
4. The API returns columns, preview rows, total row count, and filename.

### Regex Generation

1. The browser sends the pattern description, selected column, and up to five
   sample values to `/api/regex/generate`.
2. `regex_generator.py` selects the configured provider.
3. The mock provider returns a deterministic email regex, or the OpenAI
   provider requests strict structured output.
4. The backend checks regex length and compiles it with Python `re`.
5. The API returns the regex, explanation, and provider name.

### Full-File Replacement

1. The browser re-uploads the original file to `/api/files/process`.
2. The backend applies the regex only to the selected column across every row.
3. The response includes a limited processed preview and full-file statistics.

Re-uploading avoids retaining files or placing the complete dataset in browser
state.

## Backend Boundaries

### API Layer

`backend/api/` defines HTTP behavior:

- request parsing and schema validation;
- route-to-service coordination;
- stable HTTP status mappings;
- the shared structured error contract.

Business logic remains in services so it can be tested without HTTP.

### File Services

`file_parser.py` owns file validation, parsing, preview limits, and JSON-safe
value conversion.

`file_processor.py` reuses parsing rules and coordinates complete-file
replacement.

### Regex Services

`regex_generator.py` owns provider selection and local output validation.

`openai_llm.py` owns OpenAI SDK calls, Structured Outputs, provider error
mapping, refusal handling, and incomplete-response handling.

`replacement.py` owns column-scoped substitution and statistics.

## Frontend Boundaries

`App.tsx` coordinates the workflow and owns transient browser state.

`services/apiClient.ts` owns base URL configuration, request timeouts, response
parsing, and conversion of backend failures into `ApiClientError`.

Components are limited to rendering tables, status messages, and the
application-level error fallback.

## Data and Persistence

The application has no persistent database because it currently stores no
users, sessions, files, jobs, or saved transformations.

- Uploaded files exist only during request processing.
- The frontend retains the selected local `File` object for re-upload.
- Generated regex and processed rows exist only in browser memory.
- OpenAI requests use `store=false`.

A database becomes appropriate when the product adds authentication, saved
projects, job history, audit records, or queued processing.

## Error Contract

Application and validation failures use one response shape:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable corrective message.",
    "details": {}
  }
}
```

The frontend keeps the interface mounted for API, network, timeout, invalid
response, and render failures.

## Production Controls

- `DEBUG=false`
- explicit Django secret
- Render hostname validation
- HTTPS redirect and secure cookies
- exact-origin CORS
- WhiteNoise static-file handling
- upload, row, text, sample, and regex limits
- OpenAI timeout, retry, reasoning, and output-token limits

The main unresolved execution risk is catastrophic regex backtracking. Compile
and length validation do not provide an execution timeout.
