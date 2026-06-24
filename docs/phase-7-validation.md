# Phase 7 Validation Checklist

Phase 7 goal: make the application stable, reviewable, and repeatably verifiable beyond a single successful demo.

## Deliverables

- [x] Backend unit and integration tests.
- [x] Frontend manual test checklist.
- [x] Error handling matrix.
- [x] Structured request-validation errors.
- [x] Input length and row limits.
- [x] Frontend network timeout and unavailable-backend handling.
- [x] React error boundary.
- [x] Backend one-command quality check.
- [x] Frontend one-command quality check.
- [x] Shared formatting rules through `.editorconfig`.
- [x] Known limits documented.

## Validation Commands

Backend:

```powershell
Set-Location backend
& "$env:TEMP\rrapp-venv-phase5\Scripts\python.exe" .\scripts\quality_check.py
```

Result:

```text
Django system check: passed
Tests at Phase 7 completion: 37 passed
Current suite after Phase 7.5: 47 passed
```

Frontend:

```powershell
Set-Location frontend
npm.cmd run check
```

Result:

```text
Strict TypeScript check: passed
Vite production build: passed
```

## Acceptance Criteria

- [x] Invalid files have clear errors.
- [x] Invalid regex has a clear error.
- [x] Empty input has a clear error.
- [x] Missing columns have clear errors.
- [x] Mock LLM failure has a clear error.
- [x] Schema and malformed-body errors use the common API contract.
- [x] API errors do not unmount the frontend.
- [x] Unexpected render errors do not produce a blank page.
- [x] README lists current limitations.
