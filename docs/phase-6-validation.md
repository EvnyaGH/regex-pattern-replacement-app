# Phase 6 Validation Checklist

Phase 6 goal: establish a repeatable frontend-to-backend MVP flow and ensure replacement covers the complete uploaded file.

## Implemented

- [x] Frontend and backend use compatible local addresses.
- [x] CORS allows both `localhost:5173` and `127.0.0.1:5173`.
- [x] Vite can serve the frontend from the current Windows workspace path.
- [x] Frontend re-uploads the original file for replacement.
- [x] Backend processes every row and limits only the returned result preview.
- [x] Sample data remains available under `samples/`.
- [x] Local setup and flow are documented in README.
- [x] Backend integration coverage includes the PDF email example.

## Path Compatibility

The workspace path contains a literal `%`, which causes Vite 7 module URLs to return `Malformed URI sequence` on Windows even when the server reports ready.

`frontend/scripts/run-vite.mjs` temporarily maps the frontend directory to an available Windows drive letter and starts Vite from that short path. A small Vite compatibility plugin keeps the internal client environment module virtual so it cannot resolve back to the original path. The source directory is unchanged.

Validation from the original workspace:

```text
Frontend HTTP status: 200
Recursively requested frontend modules: 16
Failed module requests: 0
Malformed original-path references: 0
```

## Full-File Validation

A generated 60-row CSV was processed with a response preview limit of 50:

```text
Total rows: 60
Returned preview rows: 50
Replacement count: 60
Affected rows: 60
```

This proves the preview limit does not truncate processing.

## Automated Validation

```powershell
Set-Location backend
& "$env:TEMP\rrapp-venv-phase5\Scripts\python.exe" manage.py test

Set-Location ..\frontend
npm.cmd run build
```

Current results:

```text
Backend tests: 28 passed
Frontend production build: passed
```

## Manual Browser Check

- [x] Open the frontend in a browser and click through upload, generate, replace, and result display using `samples/email_sample.csv`.
- [x] Confirm three email addresses become `REDACTED`.
- [x] Confirm replacement statistics show three replacements across three rows.
