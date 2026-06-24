# Regex Pattern Replacement Web App

This project is a Django + React web application for uploading CSV/Excel files, using natural language to generate regex patterns, and replacing matched values in text columns.

The project is based on the technical assessment brief: `Web Application for Regex Pattern Matching and Replacement.pdf`.

Repository: https://github.com/EvnyaGH/regex-pattern-replacement-app

## Current Status

Phase 8 deployment preparation is implemented:

- Django backend project exists under `backend/`.
- Django Ninja API is configured.
- `GET /api/health` returns `{"status": "ok"}`.
- `POST /api/files/preview` accepts `.csv` and `.xlsx` uploads.
- The preview API returns filename, columns, preview rows, total row count, and preview limit.
- `POST /api/files/process` re-uploads and processes the complete source file while returning a limited result preview.
- `POST /api/regex/generate` supports deterministic mock generation or real OpenAI generation.
- `POST /api/regex/replace` applies a regex to the selected column and returns processed rows.
- React + Vite + TypeScript frontend exists under `frontend/`.
- Frontend supports file upload, preview, regex generation, replacement, and result display.
- Replacement statistics cover every row in the uploaded file, not only the displayed preview.
- Django system check and backend tests pass.
- Frontend TypeScript and Vite production build pass with x64 Node.
- API request validation uses the same structured error contract as service errors.
- Frontend handles API failures, unavailable backend, timeouts, invalid responses, and render failures without a blank page.
- OpenAI integration uses the Responses API, strict Structured Outputs, `store=false`, configurable timeout/retries, and local regex validation.
- A real OpenAI smoke test successfully generated and validated an Australian mobile-number regex.
- Render and Vercel deployment configuration is versioned in the repository.
- Django production settings include HTTPS, host, secret, static-file, and CORS controls.
- The source repository is public on GitHub.
- Public application deployment remains pending the Render and Vercel account steps.

## MVP Scope

The minimum viable product will support:

- Uploading CSV and Excel files.
- Previewing uploaded data as a table.
- Selecting a target text column.
- Describing a pattern in natural language.
- Generating a regex pattern through either the mock or OpenAI provider.
- Replacing matched values in the selected column.
- Displaying processed output data.
- Providing setup instructions, tests, deployment URL, and demo video.

## Planned Technology Stack

Backend:

- Django
- Django Ninja
- pandas
- openpyxl
- Python `re`
- pytest or Django TestCase

Frontend:

- React
- Vite
- TypeScript
- Plain CSS
- fetch

Deployment:

- Frontend: Vercel
- Backend: Render

Runtime:

- Backend Python version: 3.12

## Documentation

Project documentation is maintained under `docs/`.

- `docs/requirements.md`: project requirements, MVP scope, optional scope, and acceptance criteria.
- `docs/architecture.md`: system architecture, data flow, and module responsibilities.
- `docs/api.md`: planned API endpoints and request/response contracts.
- `docs/decision-log.md`: technical decisions and rationale.
- `docs/llm-integration.md`: mock/OpenAI providers, configuration, Structured Outputs, failures, and smoke testing.
- `docs/data-processing.md`: preview and complete-file processing behavior.
- `docs/test-plan.md`: automated coverage and manual frontend checklist.
- `docs/error-handling.md`: backend/client error matrix and configured limits.
- `docs/deployment.md`: Render/Vercel deployment procedure and environment variables.
- `docs/phase-0-validation.md` through `docs/phase-8-validation.md`: phase verification checklists.

## Local Development

### Backend

If this repository is located in a deep Windows path, creating `.venv` inside the project can hit Windows path-length limits during dependency installation. In that case, create the virtual environment in a short path such as `%TEMP%`.

PowerShell example:

```powershell
$venv = Join-Path $env:TEMP "rrapp-venv"
python -m venv $venv
& (Join-Path $venv "Scripts\python.exe") -m pip install -r backend\requirements.txt

Set-Location backend
& (Join-Path $venv "Scripts\python.exe") manage.py check
& (Join-Path $venv "Scripts\python.exe") manage.py test
& (Join-Path $venv "Scripts\python.exe") manage.py runserver
```

If the project is cloned into a short path, a local project venv is also fine:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### Frontend

Use x64 Node `20.19+` or `22.12+`. This workspace is currently validated with Chocolatey-installed Node `24.17.0`:

```powershell
& "C:\Program Files\nodejs\node.exe" -p "process.version + ' ' + process.arch + ' ' + process.execPath"
```

```powershell
Set-Location frontend
npm.cmd install
npm.cmd run build
npm.cmd run dev
```

Use `npm.cmd` directly on PowerShell because the local execution policy may block `npm.ps1`:

```powershell
& "C:\Program Files\nodejs\npm.cmd" install
& "C:\Program Files\nodejs\npm.cmd" run build
& "C:\Program Files\nodejs\npm.cmd" run dev
```

The workspace parent directory contains a literal `%`. Vite 7 cannot serve modules directly from that Windows path. The `dev` and `preview` scripts temporarily map the frontend directory to an available Windows drive letter, start Vite through that short path, and remove the mapping when the process exits. Source files remain in the project directory.

If an existing terminal still cannot find `node` after the Node upgrade, prepend the new install path for that terminal or restart the terminal:

```powershell
$env:PATH = "C:\Program Files\nodejs;$env:PATH"
node -p "process.version + ' ' + process.arch + ' ' + process.execPath"
```

Current structure:

```text
backend/
frontend/
samples/
docs/
README.md
.env.example
```

## Quality Checks

Backend:

```powershell
Set-Location backend
& "$env:TEMP\rrapp-venv-phase5\Scripts\python.exe" .\scripts\quality_check.py
```

Frontend:

```powershell
Set-Location frontend
npm.cmd run check
```

Production-mode backend:

```powershell
Set-Location backend
& "$env:TEMP\rrapp-venv-phase5\Scripts\python.exe" .\scripts\production_check.py
```

## Real LLM

The default provider remains `mock` so local development and automated tests are deterministic.

To use OpenAI in the current PowerShell session:

```powershell
$env:LLM_PROVIDER = "openai"
$env:OPENAI_API_KEY = "<your key>"
$env:LLM_MODEL = "gpt-5.5"
```

Restart the Django backend after setting the variables. Never commit or paste the real API key into source files.

Run one direct real-provider smoke test:

```powershell
Set-Location backend
& "$env:TEMP\rrapp-venv-phase5\Scripts\python.exe" .\scripts\openai_smoke_test.py
```

This command makes a real API request and may incur cost.

## Deployment

The selected production topology is:

- Frontend: Vercel
- Backend: Render
- Database: none for the stateless MVP

Deployment configuration:

- `render.yaml`
- `frontend/vercel.json`
- `docs/deployment.md`

Public URLs will be added here after the external deployments are created:

```text
Frontend URL: pending
Backend URL: pending
```

Follow `docs/deployment.md` to deploy the backend first, deploy the frontend
with the Render API URL, and then restrict Render CORS to the final Vercel
origin.

## Demo Flow

The core demo will reproduce the PDF example:

1. Upload `samples/email_sample.csv`, which contains an `Email` column.
2. Enter natural language: `Find email addresses in the Email column and replace them with 'REDACTED'.`
3. Generate a regex pattern.
4. Re-upload the original file through the processing API and replace matched email addresses with `REDACTED` across all rows.
5. Display a processed preview and full-file replacement statistics.

## Known Limits

- Mock LLM regex generation supports email address patterns only; use `LLM_PROVIDER=openai` for broader descriptions.
- Automated tests do not send paid OpenAI requests; the separate live smoke test has passed.
- Deployment configuration is complete, but public URLs require external platform account setup.
- Processed output is previewed in the browser; CSV download is not implemented yet.
- Regex is compile-checked and length-limited, but Python `re` execution does not currently have a timeout.
- Frontend automated browser tests are not included; Phase 7 uses strict TypeScript/build checks and a documented manual checklist.
