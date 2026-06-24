# Testing

## Goals

- Keep parsing, generation, and replacement independently testable.
- Verify complete-file behavior beyond the browser preview limit.
- Keep external OpenAI calls out of the deterministic automated suite.
- Verify stable API error contracts and configured limits.
- Prevent API and rendering failures from producing a blank interface.
- Validate production security, HTTPS, and CORS settings.

## Backend Suite

Run:

```powershell
Set-Location .\backend
& "..\.venv\Scripts\python.exe" .\scripts\quality_check.py
```

The command compiles Python source in memory, runs Django system checks, and
executes the complete Django test suite.

Current coverage includes:

- health endpoint, API documentation, and CORS;
- CSV and XLSX preview;
- unsupported, empty, oversized, and corrupt files;
- preview and row limits;
- mock generation in English and Chinese;
- sample-driven email generation;
- OpenAI Structured Outputs request configuration;
- OpenAI success and provider failure mappings;
- incomplete, refused, and invalid model responses;
- regex compilation and length limits;
- target-column validation;
- replacement counts, no-match behavior, and empty replacement;
- complete-file processing beyond the response preview;
- malformed JSON and missing request fields;
- end-to-end generation followed by replacement.

The current suite contains 48 tests.

## Production Backend Check

Run:

```powershell
Set-Location .\backend
& "..\.venv\Scripts\python.exe" .\scripts\production_check.py
```

The check verifies:

- Django deployment checks;
- production HTTPS health response;
- exact-origin CORS;
- HTTP-to-HTTPS redirect;
- cross-origin JSON POST behavior.

HSTS `includeSubDomains` and preload remain intentionally disabled until a
custom-domain policy is selected.

## Frontend Check

Run:

```powershell
Set-Location .\frontend
npm.cmd run check
```

The command performs strict TypeScript compilation and a Vite production build.

## Live OpenAI Check

Automated tests use fake clients. A live provider check is explicit:

```powershell
Set-Location .\backend
& "..\.venv\Scripts\python.exe" .\scripts\openai_smoke_test.py
```

This requires `OPENAI_API_KEY`, uses network access, and can incur cost.

## Browser Workflow

### Successful Flow

- [x] Load the production frontend.
- [x] Upload `samples/email_sample.csv`.
- [x] Preview three rows and the expected columns.
- [x] Generate an email regex.
- [x] Replace with `REDACTED`.
- [x] Confirm three replacements and three affected rows.
- [x] Confirm non-target columns remain unchanged.
- [x] Generate an Australian mobile-number regex through OpenAI.

### Input Failures

- [ ] Upload an unsupported file and confirm the file-type message.
- [ ] Upload an empty CSV and confirm the empty-file message.
- [ ] Submit an unsupported mock request and confirm the interface remains
  usable.
- [ ] Confirm action buttons remain disabled until required state exists.

### Network Failures

- [ ] Stop the local backend while leaving the frontend open.
- [ ] Trigger a preview request.
- [ ] Confirm the interface reports backend unavailability.
- [ ] Restart the backend and retry without refreshing the page.

### State Reset

- [ ] Complete one replacement.
- [ ] Select a different file.
- [ ] Confirm previous preview, regex, result, statistics, and errors are
  cleared.

## Test Data

- `samples/email_sample.csv` provides the public email-redaction example.
- Backend tests generate larger CSV content to verify full-file processing.
- Backend tests create XLSX workbooks in memory instead of committing binary
  fixtures.

## Release Validation

- [x] 48 backend tests pass.
- [x] Frontend TypeScript and production build pass.
- [x] Production Django checks pass.
- [x] Public health endpoint and API documentation return HTTP 200.
- [x] Production CORS preflight accepts the exact Vercel origin.
- [x] Public file preview and full-file replacement succeed.
- [x] Public OpenAI generation succeeds.
