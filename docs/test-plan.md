# Test Plan

## Goals

- Verify the PDF email-redaction workflow.
- Keep parsing, generation, and replacement logic independently testable.
- Verify API error contracts and configured input limits.
- Prevent frontend API failures from producing a blank page.
- Keep validation reproducible with one command per application.

## Automated Backend Coverage

The Django test suite covers:

- health endpoint and CORS;
- CSV and XLSX preview;
- unsupported, empty, oversized, and corrupt files;
- preview limits;
- English and Chinese email descriptions;
- sample-driven mock generation;
- OpenAI provider selection and strict Structured Outputs request configuration;
- OpenAI success, missing-key, timeout, connection, authentication, rate-limit, status, refusal, incomplete, and invalid-response behavior;
- empty, unsupported, and over-limit generation input;
- regex compilation and length limits;
- target-column validation;
- replacement counts and no-match behavior;
- empty replacement values;
- complete-file processing beyond the preview limit;
- row and replacement length limits;
- malformed JSON and missing request fields;
- the PDF generate-then-replace integration flow.

Run:

```powershell
Set-Location backend
& "$env:TEMP\rrapp-venv-phase5\Scripts\python.exe" .\scripts\quality_check.py
```

The script performs:

1. Python source syntax compilation in memory.
2. Django system check.
3. Complete Django test suite.

## Automated Frontend Checks

Run:

```powershell
Set-Location frontend
npm.cmd run check
```

The command performs:

1. strict TypeScript compilation;
2. Vite production build.

## Manual Frontend Checklist

### Happy Path

- [ ] Start backend and frontend.
- [ ] Upload `samples/email_sample.csv`.
- [ ] Confirm three rows and the `ID`, `Name`, and `Email` columns appear.
- [ ] Generate the email regex.
- [ ] Replace with `REDACTED`.
- [ ] Confirm three replacements and three affected rows.
- [ ] Confirm non-target columns remain unchanged.

### Input Errors

- [ ] Upload a `.txt` file and confirm an unsupported-file message appears.
- [ ] Upload an empty `.csv` and confirm an empty-file message appears.
- [ ] Enter an unsupported mock description such as `Find product SKUs` and confirm generation fails without a blank page.
- [ ] Confirm action buttons remain disabled when required preceding state is unavailable.

### Network Errors

- [ ] Stop the backend while leaving the frontend open.
- [ ] Click `Preview data`.
- [ ] Confirm the page shows `Backend is unavailable`.
- [ ] Restart the backend and confirm the workflow can be retried.

### State Reset

- [ ] Process one file successfully.
- [ ] Select a different file.
- [ ] Confirm old preview, regex, result, statistics, and errors are cleared.

## Test Data

- `samples/email_sample.csv`: canonical PDF flow.
- Generated CSV content in backend tests: verifies files larger than the preview.
- In-memory XLSX workbooks in backend tests: avoids committing opaque binary fixtures.

## Final Acceptance

- [x] Backend quality command passes.
- [x] Frontend quality command passes.
- [x] Phase 6 browser happy path passes.
- [x] Error cases have structured backend responses.
- [x] Frontend catches API, timeout, network, invalid-response, and render errors.
