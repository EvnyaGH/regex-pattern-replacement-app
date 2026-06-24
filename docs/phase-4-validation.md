# Phase 4 Validation Checklist

Phase 4 goal: apply a regex replacement to a selected column and return processed data with replacement statistics.

## Deliverables

- [x] `POST /api/regex/replace` exists.
- [x] Replacement request schema exists.
- [x] Replacement response schema exists.
- [x] Replacement service exists.
- [x] Regex is compiled and validated before replacement.
- [x] Replacement applies only to the selected target column.
- [x] Non-target columns are preserved.
- [x] Empty replacement value is allowed.
- [x] No-match cases return success with zero counts.
- [x] PDF email redaction example is tested.
- [x] Generate-then-replace backend flow is tested.
- [x] API documentation is updated.

## Implemented Endpoint

```text
POST /api/regex/replace
```

Example request:

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

Expected response:

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

## Error Codes

| Code | Meaning |
|---|---|
| `MISSING_TARGET_COLUMN` | Target column is empty. |
| `TARGET_COLUMN_NOT_FOUND` | Target column does not exist in the provided columns. |
| `INVALID_REGEX` | Regex is empty or cannot be compiled. |
| `NO_ROWS` | Request contains no rows. |

## Replacement Semantics

- Replacement is applied only to `target_column`.
- `replacement_count` is the total number of regex matches replaced.
- `affected_row_count` is the number of rows with at least one replacement.
- If a row has no match, the original value is preserved.
- If the target value is `null`, it is preserved.
- Empty replacement string is allowed and deletes matched content.

## Validation Commands

Validation was run from:

```text
Internship/regex-pattern-replacement-app/backend
```

The same short-path virtual environment workaround from earlier phases was used:

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
Found 24 test(s).
System check identified no issues (0 silenced).
........................
----------------------------------------------------------------------
Ran 24 tests

OK
```

## Explainability Checks

- [x] Replacement logic is isolated in `services/replacement.py`.
- [x] API route delegates to the service layer.
- [x] Replacement counting semantics are documented.
- [x] Error behavior is documented.

## Repeatability Checks

- [x] PDF example data is embedded in tests.
- [x] Backend generate-then-replace flow is tested without external services.
- [x] Tests do not require network access.
- [x] No database or file persistence is required.

## Verifiability Checks

- [x] `manage.py check` passes.
- [x] `manage.py test` passes.
- [x] Successful replacement path is tested.
- [x] Multiple matches in one row are tested.
- [x] No-match success path is tested.
- [x] Missing target column is tested.
- [x] Unknown target column is tested.
- [x] Invalid regex is tested.
- [x] Empty regex is tested.
- [x] Empty replacement string is tested.

## Remaining Before Phase 5

- [ ] Scaffold React + Vite + TypeScript frontend.
- [ ] Implement file upload UI.
- [ ] Implement preview table UI.
- [ ] Implement regex generation UI.
- [ ] Implement replacement result UI.
- [ ] Wire frontend API calls to backend endpoints.
