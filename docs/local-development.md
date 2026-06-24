# Local Development

## Requirements

- Python 3.12
- Node.js 22.12 or newer
- npm

The backend runtime is pinned in `backend/.python-version`. Frontend runtime
requirements are declared in `frontend/package.json`.

## Backend Setup

### Windows PowerShell

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt

Set-Location .\backend
& "..\.venv\Scripts\python.exe" manage.py runserver
```

### macOS or Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py runserver
```

The backend starts at `http://127.0.0.1:8000`. Useful endpoints:

- `http://127.0.0.1:8000/api/health`
- `http://127.0.0.1:8000/api/docs`

On Windows, a deeply nested repository path can exceed dependency-installation
path limits. Use a short virtual-environment path when that occurs:

```powershell
$venv = Join-Path $env:TEMP "rrapp-venv"
python -m venv $venv
& (Join-Path $venv "Scripts\python.exe") -m pip install -r .\backend\requirements.txt
```

## Frontend Setup

In another terminal:

```powershell
Set-Location .\frontend
npm.cmd install
npm.cmd run dev
```

On macOS or Linux, use `npm` instead of `npm.cmd`.

The frontend starts at `http://127.0.0.1:5173`.

## Local Configuration

The application reads environment variables from the process. It does not load
`.env` automatically.

Default local behavior:

```text
LLM_PROVIDER=mock
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

The mock provider is deterministic and supports the email example without
network access or credentials.

Enable OpenAI in the terminal that starts Django:

```powershell
$env:LLM_PROVIDER = "openai"
$env:OPENAI_API_KEY = "<your key>"
$env:LLM_MODEL = "gpt-5.5"
```

Restart Django after changing backend environment variables.

Frontend `VITE_*` variables are read when Vite starts or builds. Restart Vite
after changing them.

## Quality Commands

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

The live OpenAI smoke test is separate because it requires a secret, network
access, and a potentially billable request:

```powershell
Set-Location .\backend
& "..\.venv\Scripts\python.exe" .\scripts\openai_smoke_test.py
```

## Windows Path Compatibility

Vite can fail with `URI malformed` when the absolute workspace path contains a
literal `%`. The `dev` and `preview` scripts use
`frontend/scripts/run-vite.mjs` to create a temporary drive mapping and launch
Vite from a safe short path.

The mapping is removed when the process exits normally. A repository cloned to
a conventional development path does not need this workaround.

PowerShell execution policy can also block `npm.ps1`; use `npm.cmd` when that
occurs.

## Environment Reference

`.env.example` lists all supported variables. Important groups:

- Django production and security settings;
- CORS and trusted origins;
- file, row, text, sample, and regex limits;
- frontend API URL and timeout;
- OpenAI provider, model, timeout, retries, and output budget.
