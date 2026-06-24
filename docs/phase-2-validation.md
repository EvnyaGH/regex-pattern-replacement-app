# Phase 2 Validation Checklist

Phase 2 goal: implement CSV/Excel upload preview through the backend API.

## Deliverables

- [x] `POST /api/files/preview` exists.
- [x] CSV parsing is supported.
- [x] `.xlsx` parsing is supported.
- [x] Preview response includes filename, columns, rows, row count, and preview limit.
- [x] Unsupported file types return a structured error.
- [x] Empty files return a structured error.
- [x] Oversized files return a structured error.
- [x] Invalid preview limits return a structured error.
- [x] Sample CSV exists at `samples/email_sample.csv`.
- [x] File preview API tests exist.
- [x] API documentation is updated.

## Implemented Endpoint

```text
POST /api/files/preview
```

Request type:

```text
multipart/form-data
```

Fields:

| Field | Required | Description |
|---|---|---|
| `file` | Yes | `.csv` or `.xlsx` file |
| `preview_limit` | No | Rows to preview; defaults to 50 |

Expected successful response:

```json
{
  "filename": "email_sample.csv",
  "columns": ["ID", "Name", "Email"],
  "rows": [
    {"ID": 1, "Name": "John Doe", "Email": "john.doe@example.com"}
  ],
  "row_count": 3,
  "preview_limit": 1
}
```

## Error Codes

| Code | Meaning |
|---|---|
| `INVALID_FILE_TYPE` | File extension is not `.csv` or `.xlsx`. |
| `EMPTY_FILE` | Uploaded file has no readable content. |
| `FILE_PARSE_ERROR` | pandas/openpyxl could not parse the file. |
| `FILE_TOO_LARGE` | File exceeds `MAX_UPLOAD_BYTES`. |
| `INVALID_PREVIEW_LIMIT` | Preview limit is outside the configured range. |

## Validation Commands

Validation was run from:

```text
Internship/regex-pattern-replacement-app/backend
```

The same short-path virtual environment workaround from Phase 1 was used because the workspace path is long on Windows:

```text
%TEMP%/rrapp-phase1-venv
```

### Install Updated Dependencies

Command:

```powershell
& (Join-Path $env:TEMP "rrapp-phase1-venv\Scripts\python.exe") -m pip install -r backend\requirements.txt
```

Result:

```text
Successfully installed pandas, openpyxl, and transitive dependencies.
```

### Django System Check

Command:

```powershell
& (Join-Path $env:TEMP "rrapp-phase1-venv\Scripts\python.exe") manage.py check
```

Expected result:

```text
System check identified no issues (0 silenced).
```

### Django Tests

Command:

```powershell
& (Join-Path $env:TEMP "rrapp-phase1-venv\Scripts\python.exe") manage.py test
```

Expected result:

```text
Found 7 test(s).
System check identified no issues (0 silenced).
.......
----------------------------------------------------------------------
Ran 7 tests

OK
```

## Explainability Checks

- [x] File parsing logic is isolated in `services/file_parser.py`.
- [x] API route code delegates to the service layer.
- [x] Response schemas are separated from implementation.
- [x] Error responses follow the documented common error shape.

## Repeatability Checks

- [x] Required parsing dependencies are in `backend/requirements.txt`.
- [x] File size and preview row limits are configurable through `.env.example`.
- [x] Sample CSV is committed under `samples/`.
- [x] Tests generate their own in-memory Excel file.

## Verifiability Checks

- [x] `manage.py check` passes.
- [x] `manage.py test` passes.
- [x] CSV success path is tested.
- [x] Excel success path is tested.
- [x] Invalid type, empty file, oversized file, and invalid preview limit are tested.

## Remaining Before Phase 3

- [ ] Implement regex generation service.
- [ ] Add mock LLM behavior for common email pattern input.
- [ ] Add `POST /api/regex/generate`.
- [ ] Validate generated regex with Python `re.compile`.
