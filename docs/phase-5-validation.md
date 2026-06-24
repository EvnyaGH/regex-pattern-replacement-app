# Phase 5 Validation Checklist

Phase 5 goal: implement the React frontend workflow for upload, preview, regex generation, replacement, and result display.

## Deliverables

- [x] `frontend/` directory exists.
- [x] Vite + React + TypeScript project files exist.
- [x] API client exists.
- [x] TypeScript API response types exist.
- [x] File upload UI exists.
- [x] Data preview table exists.
- [x] Target column selector exists.
- [x] Natural language input exists.
- [x] Regex generation button exists.
- [x] Replacement input exists.
- [x] Replacement action button exists.
- [x] Processed result table exists.
- [x] Loading and error states exist.
- [x] Frontend build is validated with x64 Node.

## Implemented Frontend Flow

1. User selects a `.csv` or `.xlsx` file.
2. User clicks `Preview data`.
3. Frontend calls `POST /api/files/preview`.
4. Frontend renders returned columns and rows.
5. User selects a target column.
6. User enters a natural language pattern description.
7. User clicks `Generate regex`.
8. Frontend calls `POST /api/regex/generate`.
9. Frontend displays generated regex and explanation.
10. User enters a replacement value.
11. User clicks `Replace matches`.
12. Frontend calls `POST /api/regex/replace`.
13. Frontend renders processed rows and replacement statistics.

## Key Files

| File | Purpose |
|---|---|
| `frontend/src/App.tsx` | Main workflow state and UI composition. |
| `frontend/src/services/apiClient.ts` | Backend API calls and structured error handling. |
| `frontend/src/types/api.ts` | API request/response TypeScript types. |
| `frontend/src/components/DataTable.tsx` | Preview/result table rendering. |
| `frontend/src/components/StatusMessage.tsx` | Error and success state rendering. |
| `frontend/src/styles.css` | Responsive operational UI styling. |

## Validation Environment

The original local system Node installation was not suitable for this Vite version:

```text
Original system Node: v20.18.0 ia32
Bundled Node: v24.14.0 x64
```

Vite 7 requires x64 Node `20.19+` or `22.12+`. Initial validation used bundled Node `24.14.0`.

Global Node was then upgraded with Chocolatey from an elevated PowerShell:

```powershell
choco install nodejs-lts -y --x64
```

Confirmed installed package and runtime:

```text
nodejs-lts|24.17.0
v24.17.0 x64 C:\Program Files\nodejs\node.exe
npm 11.13.0
```

The current Codex process still had the old inherited `PATH`, so validation prepended the new install path for this terminal:

```powershell
$env:PATH = "C:\Program Files\nodejs;$env:PATH"
```

## Validation Commands

Install dependencies with the upgraded Node and a project-local npm cache:

```powershell
$env:PATH = "C:\Program Files\nodejs;$env:PATH"
& "C:\Program Files\nodejs\npm.cmd" install --cache .\.npm-cache --include=optional --no-audit --no-fund
```

Build validation:

```powershell
& "C:\Program Files\nodejs\npm.cmd" run build
```

Build result:

```text
v24.17.0 x64 C:\Program Files\nodejs\node.exe
vite v7.3.5 building client environment for production...
1582 modules transformed.
dist/index.html
dist/assets/index-*.css
dist/assets/index-*.js
built in 2.92s
```

The build script calls tool entrypoints through `node ./node_modules/...` rather than relying on Windows `.cmd` shims. This avoids command parsing issues caused by the workspace path containing `&`.

The development and preview scripts use `frontend/scripts/run-vite.mjs`. The launcher creates a temporary Windows drive mapping when the workspace contains `%`, avoiding malformed Vite module URLs.

Dev server smoke test:

```powershell
& "C:\Program Files\nodejs\npm.cmd" run dev -- --port 5173
```

Result:

```text
VITE v7.3.5 ready in 396 ms
Local: http://127.0.0.1:5173/
```

## Explainability Checks

- [x] API calls are isolated in `apiClient.ts`.
- [x] Backend response shapes are typed in `types/api.ts`.
- [x] UI state follows the backend flow: preview -> generate -> replace.
- [x] Errors from backend structured responses are displayed to the user.

## Repeatability Checks

- [x] `package.json` defines install/build/dev scripts.
- [x] `package-lock.json` records resolved npm dependencies.
- [x] README states the x64 Node requirement.
- [x] Frontend uses `VITE_API_BASE_URL` with a default of `http://localhost:8000/api`.

## Verifiability Checks

- [x] TypeScript compilation passes.
- [x] Vite production build passes.
- [x] Vite development server serves the homepage with HTTP 200 from the current workspace.
- [x] UI has controls for all Phase 5 workflow steps.
- [x] UI has disabled/loading/error states.

## Completed in Phase 6

- [x] Run backend and frontend together for HTTP-level workflow validation.
- [x] Add end-to-end flow documentation for the local demo.
- [x] Process complete files instead of only preview rows.
- [ ] Manually complete the browser workflow using `samples/email_sample.csv`.
- [ ] Decide whether frontend automated tests are needed before deployment.
