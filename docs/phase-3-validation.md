# Phase 3 Validation Checklist

Phase 3 goal: implement deterministic regex generation through a mock LLM provider.

## Deliverables

- [x] `POST /api/regex/generate` exists.
- [x] Regex request schema exists.
- [x] Regex response schema exists.
- [x] Mock regex generation service exists.
- [x] Generated regex is validated with Python `re.compile`.
- [x] Email address descriptions return a valid email regex.
- [x] Chinese email-related descriptions are supported.
- [x] Email-like sample values can trigger email regex generation.
- [x] Empty natural language descriptions return a structured error.
- [x] Missing target column returns a structured error.
- [x] Unsupported mock descriptions return `LLM_GENERATION_FAILED`.
- [x] API documentation is updated.
- [x] LLM integration documentation exists.

## Implemented Endpoint

```text
POST /api/regex/generate
```

Example request:

```json
{
  "natural_language": "Find email addresses in the Email column",
  "target_column": "Email",
  "sample_values": [
    "john.doe@example.com",
    "jane_smith@domain.com"
  ]
}
```

Expected successful response:

```json
{
  "regex": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,7}\\b",
  "explanation": "Matches common email addresses using local-part, domain, and TLD groups.",
  "provider": "mock"
}
```

## Error Codes

| Code | Meaning |
|---|---|
| `EMPTY_DESCRIPTION` | Natural language input is empty. |
| `MISSING_TARGET_COLUMN` | Target column is empty. |
| `LLM_GENERATION_FAILED` | Mock provider cannot generate a regex for the description. |
| `INVALID_GENERATED_REGEX` | Generated regex cannot be compiled. |

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
Found 14 test(s).
System check identified no issues (0 silenced).
..............
----------------------------------------------------------------------
Ran 14 tests

OK
```

## Explainability Checks

- [x] Mock LLM scope is documented.
- [x] The reason for limiting mock support to email patterns is documented.
- [x] API route delegates regex generation to the service layer.
- [x] Generated regex validation is explicit.

## Repeatability Checks

- [x] Mock provider behavior is deterministic.
- [x] No external LLM credentials are required.
- [x] Tests do not require network access.
- [x] API request and response examples are documented.

## Verifiability Checks

- [x] `manage.py check` passes.
- [x] `manage.py test` passes.
- [x] English email request is tested.
- [x] Chinese email request is tested.
- [x] Sample-value inference is tested.
- [x] Error branches are tested.

## Remaining Before Phase 4

- [ ] Implement regex replacement service.
- [ ] Add `POST /api/regex/replace`.
- [ ] Apply regex only to the selected target column.
- [ ] Return processed rows, replacement count, and affected row count.
- [ ] Test the PDF email redaction example end to end at the backend API layer.
