# Phase 1 Validation Checklist

Phase 1 goal: create the minimum runnable Django backend and expose a verifiable health API.

## Deliverables

- [x] `backend/` directory exists.
- [x] `backend/manage.py` exists.
- [x] `backend/requirements.txt` exists.
- [x] `backend/.python-version` records Python 3.12.13 (migrated from
  `runtime.txt` during Phase 8 to match current Render configuration).
- [x] Django settings are defined in `backend/config/settings.py`.
- [x] Django root URLs are defined in `backend/config/urls.py`.
- [x] Django Ninja API router exists in `backend/api/router.py`.
- [x] Health route exists in `backend/api/health_routes.py`.
- [x] Health response schema exists in `backend/schemas/health_schemas.py`.
- [x] Health endpoint test exists in `backend/api/tests/test_health.py`.

## Implemented Endpoint

```text
GET /api/health
```

Expected response:

```json
{
  "status": "ok"
}
```

## Validation Commands

Validation was run from:

```text
Internship/regex-pattern-replacement-app/backend
```

Because the repository path is long on Windows, dependency installation into a project-local `.venv` failed with a Windows long-path error. Validation used a short-path temporary virtual environment:

```text
%TEMP%/rrapp-phase1-venv
```

### Django System Check

Command:

```powershell
& (Join-Path $env:TEMP "rrapp-phase1-venv\Scripts\python.exe") manage.py check
```

Result:

```text
System check identified no issues (0 silenced).
```

### Django Tests

Command:

```powershell
& (Join-Path $env:TEMP "rrapp-phase1-venv\Scripts\python.exe") manage.py test
```

Result:

```text
Found 1 test(s).
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.007s

OK
```

## Explainability Checks

- [x] API route layer is separated from Django project settings.
- [x] Response schema is separated from route implementation.
- [x] Health endpoint has one narrow responsibility.
- [x] Local settings use environment variables for deployment-sensitive values.

## Repeatability Checks

- [x] Dependencies are documented in `backend/requirements.txt`.
- [x] Backend runtime is documented in `backend/.python-version`.
- [x] README includes backend setup commands.
- [x] README includes a Windows long-path workaround.

## Verifiability Checks

- [x] `manage.py check` passes.
- [x] `manage.py test` passes.
- [x] Health endpoint behavior is covered by an automated test.

## Remaining Before Phase 2

- [ ] Add file upload dependencies for CSV/Excel parsing when Phase 2 begins.
- [ ] Create sample CSV data under `samples/`.
- [ ] Implement `POST /api/files/preview`.
- [ ] Add tests for file type validation and preview output.
