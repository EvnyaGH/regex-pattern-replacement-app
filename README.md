# Regex Pattern Replacement

A web application for finding and replacing structured text patterns in CSV and
Excel files. Describe a pattern in natural language, inspect the generated
regular expression, and apply the replacement to a selected column.

## Live Application

- Web app: https://regex-pattern-replacement-app.vercel.app
- API: https://regex-pattern-replacement-api.onrender.com/api
- API documentation: https://regex-pattern-replacement-api.onrender.com/api/docs
- Source: https://github.com/EvnyaGH/regex-pattern-replacement-app

The backend runs on Render's free tier, so the first request after inactivity
can take longer than usual.

## Demo Video

[Watch the Regex Pattern Replacement demonstration on YouTube](https://youtu.be/DC5qSZYgeh8)

## Features

- Upload `.csv` and `.xlsx` files up to the configured size limit.
- Preview columns and rows before processing.
- Select one target column for transformation.
- Generate Python-compatible regex from natural-language descriptions.
- Use deterministic mock generation for offline development.
- Use OpenAI Responses API with strict Structured Outputs in production.
- Review the generated regex and explanation before replacement.
- Replace every match in the complete uploaded file.
- Display a processed preview, replacement count, and affected-row count.
- Return structured API errors for invalid files, input, regex, and provider
  failures.

## How It Works

```text
Browser
  |
  | upload and configuration
  v
React + TypeScript frontend
  |
  | HTTPS JSON and multipart requests
  v
Django Ninja API
  |
  +-- file parsing and validation
  +-- regex generation
  +-- full-file replacement
  |
  +--> OpenAI Responses API
```

The service is stateless. Files are processed in memory during each request and
are not saved by the application. The source file is uploaded once for preview
and again when the complete replacement is executed.

When the OpenAI provider is enabled, the pattern description, selected column
name, and a small set of sample values are sent to OpenAI. The request uses
`store=false`. See [Privacy and Security](docs/privacy-security.md) before
processing sensitive data.

## Quick Start

### Requirements

- Python 3.12
- Node.js 22.12 or newer
- npm

### Backend

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt

Set-Location .\backend
& "..\.venv\Scripts\python.exe" manage.py runserver
```

If PowerShell interprets the relative command above incorrectly, run:

```powershell
& (Resolve-Path "..\.venv\Scripts\python.exe") manage.py runserver
```

The local backend starts at `http://127.0.0.1:8000`.

### Frontend

In a second terminal:

```powershell
Set-Location .\frontend
npm.cmd install
npm.cmd run dev
```

The local frontend starts at `http://127.0.0.1:5173`.

Local development defaults to the deterministic `mock` provider, so no API key
is required for the email-address example.

For detailed environment configuration and Windows path notes, see
[Local Development](docs/local-development.md).

## OpenAI Provider

Set the variables in the backend process before starting Django:

```powershell
$env:LLM_PROVIDER = "openai"
$env:OPENAI_API_KEY = "<your key>"
$env:LLM_MODEL = "gpt-5.5"
```

Never commit an API key. Automated tests use fake OpenAI clients and do not make
paid requests.

One explicit live-provider smoke test is available:

```powershell
Set-Location .\backend
& "..\.venv\Scripts\python.exe" .\scripts\openai_smoke_test.py
```

This command makes a real API request and can incur cost.

## Example Workflow

Use the included [`samples/email_sample.csv`](samples/email_sample.csv):

1. Upload the sample file and select **Preview data**.
2. Select the `Email` column.
3. Enter `Find email addresses in the Email column`.
4. Generate the regex.
5. Set the replacement value to `REDACTED`.
6. Replace matches.
7. Confirm three replacements across three rows.

The same flow is available in the
[public demo](https://regex-pattern-replacement-app.vercel.app).

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | Service health |
| `POST` | `/api/files/preview` | Validate and preview CSV/XLSX |
| `POST` | `/api/files/process` | Replace matches across the complete file |
| `POST` | `/api/regex/generate` | Generate regex from natural language |
| `POST` | `/api/regex/replace` | Apply replacement to JSON rows |

See [API Reference](docs/api.md) for request, response, and error contracts.

## Quality Checks

Backend:

```powershell
Set-Location .\backend
& "..\.venv\Scripts\python.exe" .\scripts\quality_check.py
& "..\.venv\Scripts\python.exe" .\scripts\production_check.py
```

Frontend:

```powershell
Set-Location .\frontend
npm.cmd run check
```

Current validation covers 48 backend tests, strict TypeScript compilation,
Vite production build, Django deployment settings, HTTPS behavior, production
CORS, and cross-origin API requests.

## Deployment

- Frontend: Vercel
- Backend: Render
- LLM provider: OpenAI
- Database: not required by the stateless request model

Deployment configuration is versioned in [`render.yaml`](render.yaml) and
[`frontend/vercel.json`](frontend/vercel.json). See
[Deployment](docs/deployment.md) for environment variables, deployment order,
and production verification.

## Project Structure

```text
backend/                 Django Ninja API and service layer
frontend/                React, TypeScript, and Vite application
samples/                 Public sample data
docs/                    Architecture, API, operations, and engineering records
render.yaml              Render Blueprint
.env.example             Environment variable reference
```

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Data Processing](docs/data-processing.md)
- [LLM Integration](docs/llm-integration.md)
- [Error Handling](docs/error-handling.md)
- [Local Development](docs/local-development.md)
- [Deployment](docs/deployment.md)
- [Privacy and Security](docs/privacy-security.md)
- [Demo Guide](docs/demo.md)
- [Testing](docs/test-plan.md)
- [Release Notes](docs/release-notes.md)
- [Decision Log](docs/decision-log.md)

Phase validation records under `docs/phase-*-validation.md` preserve the
implementation and verification history.

## Current Limits

- The browser displays processed rows but does not yet export a processed CSV.
- Only one column can be transformed per operation.
- Python `re` execution has compile and length checks but no execution timeout;
  untrusted regex can still create ReDoS risk.
- Processing is in memory and limited by configured upload and row limits.
- The mock provider supports email-pattern generation only.
- Frontend validation currently uses TypeScript/build checks and documented
  browser workflows rather than an automated browser test suite.

## Roadmap

- Export processed data as CSV.
- Add regex execution timeout or a safer regex engine.
- Add automated browser tests.
- Support multiple target columns.
- Add queued or streaming processing for larger files.

## Contributing

Development workflow and pull-request expectations are documented in
[CONTRIBUTING.md](CONTRIBUTING.md).

Security issues should be reported through the process in
[SECURITY.md](SECURITY.md), not through a public issue containing secrets or
sensitive data.
