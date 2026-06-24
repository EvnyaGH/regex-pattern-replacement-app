# Decision Log

This document records major technical decisions. Each entry should explain the context, alternatives, decision, rationale, and expected impact.

## 2026-06-24 - Use Django and React for the project

- Context: The assessment brief explicitly requires a web application using Django and React.
- Alternatives: FastAPI, Flask, Vue, Next.js-only full stack.
- Decision: Use Django for the backend and React for the frontend.
- Rationale: This directly satisfies the brief and aligns with the expected technical assessment.
- Impact: Backend and frontend will be developed as separate projects with API-based communication.

## 2026-06-24 - Use Django Ninja for backend APIs

- Context: The backend needs clear API endpoints for file preview, regex generation, and replacement.
- Alternatives: Django REST Framework, plain Django views.
- Decision: Use Django Ninja.
- Rationale: Django Ninja provides typed schemas, simple routing, and fast setup while staying within the Django ecosystem.
- Impact: API request and response schemas will be defined explicitly and documented in `docs/api.md`.

## 2026-06-24 - Use a service layer for core logic

- Context: File parsing, regex generation, and replacement logic must be testable and maintainable.
- Alternatives: Put all logic directly in API route handlers.
- Decision: Create service modules for file parsing, regex generation, LLM calls, and replacement.
- Rationale: Service modules can be unit tested without running the HTTP server.
- Impact: API routes should stay thin and delegate business logic to services.

## 2026-06-24 - Start with mock LLM before real LLM integration

- Context: The application must use an LLM, but development should remain reproducible without API credentials.
- Alternatives: Integrate a real LLM immediately, or manually hard-code regex without an LLM abstraction.
- Decision: Implement a mock LLM provider first, then add a real LLM provider behind the same interface.
- Rationale: This allows the end-to-end flow to be developed and tested before external credentials are available.
- Impact: The LLM provider will be selected through environment configuration such as `LLM_PROVIDER=mock`.

## 2026-06-24 - Keep MVP file handling stateless

- Context: The MVP needs to preview data and apply replacement, but persistent storage is not required by the brief.
- Alternatives: Store uploaded files in a database or object storage.
- Decision: Keep MVP file handling stateless and return parsed rows to the frontend.
- Rationale: Stateless handling reduces scope and avoids authentication, cleanup, and storage security concerns.
- Impact: Large-file support will be treated as an optional enhancement rather than a Phase 1-6 requirement.

## 2026-06-24 - Use Python 3.12, Vercel, and Render

- Context: Phase 1 needs a confirmed Python version and an initial deployment target.
- Alternatives: Python 3.11, Railway, Fly.io, Netlify.
- Decision: Use Python 3.12 for the backend runtime, deploy the frontend to Vercel, and deploy the backend to Render.
- Rationale: Python 3.12 is current and well supported by the planned backend libraries. Vercel is a straightforward fit for a Vite React frontend, and Render is a straightforward fit for a Django backend using `requirements.txt`.
- Impact: Phase 1 backend setup should target Python 3.12, and deployment documentation should assume Vercel + Render unless a later constraint forces a change.

## 2026-06-24 - Keep Phase 2 file handling preview-only

- Context: Phase 2 adds CSV/Excel upload and table preview, while later phases handle regex generation and replacement.
- Alternatives: Persist uploaded files immediately, or return all rows without limits.
- Decision: Keep Phase 2 stateless and preview-only. Return parsed columns, preview rows, total row count, and configured preview limit.
- Rationale: This satisfies the file upload milestone without introducing storage, cleanup, authentication, or large-file architecture before the core flow exists.
- Impact: The frontend will initially work with preview JSON. Large-file support and persistent upload sessions remain optional enhancements.

## 2026-06-24 - Limit Phase 3 mock LLM to email regex generation

- Context: Phase 3 needs a reproducible regex generation endpoint before a real LLM provider is connected.
- Alternatives: Mock many pattern types, or call a real LLM immediately.
- Decision: Implement a deterministic mock provider that supports email address pattern generation only.
- Rationale: The PDF example centers on email redaction. Supporting one stable pattern keeps tests deterministic and avoids pretending the mock provider understands arbitrary natural language.
- Impact: Unknown pattern descriptions return `LLM_GENERATION_FAILED`. Real LLM integration remains a later enhancement behind the same service boundary.

## 2026-06-24 - Keep regex replacement stateless and column-scoped

- Context: Phase 4 needs to apply a regex to uploaded table data without introducing persistence.
- Alternatives: Store uploaded data server-side, or apply replacements across every text field automatically.
- Decision: Accept columns, rows, target column, regex, and replacement value in the request. Apply replacement only to the selected target column and return processed rows plus statistics.
- Rationale: This keeps the backend stateless, predictable, and aligned with the PDF workflow where users specify a text column.
- Impact: The frontend will pass currently loaded table data into the replacement endpoint. Persistent jobs and multi-column replacement remain later enhancements.

## 2026-06-24 - Use plain CSS for Phase 5 frontend styling

- Context: The original plan mentioned Tailwind CSS, but Phase 5 needed a working frontend workflow with minimal tooling risk.
- Alternatives: Add Tailwind immediately, or use plain CSS and keep the Vite toolchain smaller.
- Decision: Use plain CSS for Phase 5.
- Rationale: The app is an operational data tool with a compact UI. Plain CSS is sufficient for layout, responsive behavior, status states, and table styling while reducing dependency and configuration complexity.
- Impact: Tailwind remains optional. The frontend is easier to build and deploy in the current environment.

## 2026-06-24 - Require x64 Node for frontend build

- Context: The local system `npm.cmd` is bound to a 32-bit Node 20.18.0, while bundled Node 24.14.0 is x64 and satisfies Vite 7.
- Alternatives: Upgrade system Node, downgrade Vite, or validate with the bundled x64 Node.
- Decision: Do not upgrade system Node for the project. Validate and document the frontend with x64 Node 20.19+ or the bundled Node 24.14.0.
- Rationale: The project itself only requires an appropriate x64 Node runtime. Modifying the user's system Node installation is unnecessary and riskier than documenting the runtime requirement.
- Impact: README now states the x64 Node requirement. Vite scripts use `--configLoader native` to avoid config bundling issues observed in the local sandbox.

## 2026-06-24 - Use upgraded x64 Node and direct tool entrypoints for frontend scripts

- Context: The user upgraded global Node through elevated Chocolatey. The installed runtime is Node `24.17.0` x64 at `C:\Program Files\nodejs\node.exe`. The workspace path contains `&`, which caused Windows npm bin shims such as `tsc.cmd` to misparse paths during `npm run build`.
- Alternatives: Keep using the bundled Node with temporary `PATH`, move the project to a shorter path, downgrade the Vite toolchain, or call package entrypoints directly through `node`.
- Decision: Use the upgraded x64 Node for local frontend development and update npm scripts to call `node ./node_modules/...` entrypoints directly.
- Rationale: This keeps the current workspace location and avoids Windows `.cmd` shim path parsing issues while preserving the Vite 7 toolchain.
- Impact: `npm run build` now passes in the actual `frontend/` directory with Node `24.17.0` x64.

## 2026-06-24 - Re-upload the original file for stateless full-file processing

- Context: The preview API returns at most 50 rows by default. Sending those preview rows to `/regex/replace` caused files with more rows to be only partially processed.
- Alternatives: Return all uploaded rows to the browser, store uploads in a database or temporary session, or re-upload the source file when replacement is requested.
- Decision: Add `POST /api/files/process` and re-upload the original file with the regex and replacement settings.
- Rationale: This processes every row without moving the complete dataset into frontend state and preserves the no-database, stateless architecture.
- Impact: The browser receives a limited processed preview while counts represent the complete file. CSV export can reuse the same processing service later.

## 2026-06-24 - Use a temporary drive mapping for Vite on Windows paths containing percent

- Context: Vite 7 returned `URI malformed` when serving HTML from the current workspace because its absolute Windows path contains a literal `%`.
- Alternatives: Move the repository, downgrade Vite, require a manually created drive mapping, or automate a temporary mapping for development.
- Decision: Add `frontend/scripts/run-vite.mjs` to map the frontend to an available drive letter before starting Vite. Add a local Vite plugin to keep its internal environment module from resolving to the original absolute path.
- Rationale: Windows `subst` paths remain short even after `realpath`, unlike junction paths. The workaround is repeatable, does not copy data, and is unnecessary in normal clone paths or deployment environments.
- Impact: `npm.cmd run dev` now serves both the homepage and dependent modules from the existing workspace. The temporary mapping is removed when the Vite process exits normally.

## 2026-06-24 - Normalize request validation and enforce configurable input limits

- Context: Django Ninja schema errors used a different `detail` response from application errors, and several text/list inputs had no explicit upper bound.
- Alternatives: Keep framework defaults, add constraints only in Pydantic schemas, or normalize framework errors and keep domain limits in service functions.
- Decision: Register API-level handlers for validation/body errors and enforce configurable limits in the service layer.
- Rationale: Every client-visible failure now follows one contract, while service-level checks remain testable without HTTP and protect both file and JSON processing paths.
- Impact: The backend exposes additional environment limits, the frontend can display predictable messages, and the test suite covers malformed requests and boundary failures.

## 2026-06-24 - Add OpenAI Responses API as the real LLM provider

- Context: The assessment requires LLM-backed natural-language regex generation, while the existing deterministic mock only supports email examples.
- Alternatives: Replace the mock entirely, call OpenAI directly from API routes, use free-form text output, or add OpenAI behind the existing provider boundary.
- Decision: Keep mock as the default test provider and add an `openai` provider using the official Python SDK, Responses API, strict Structured Outputs, and `store=false`.
- Rationale: Mock preserves deterministic and credential-free verification. Structured Outputs provides a stable `regex` and `explanation` contract, while the service boundary contains external API behavior and failures.
- Impact: Deployments can enable real generation with `LLM_PROVIDER=openai`. External calls require a secret and may incur cost. Generated regex still passes local length and compile validation, but stronger ReDoS protection remains future work.

## 2026-06-24 - Deploy the stateless MVP without a production database

- Context: Phase 8 needs a public backend on Render. The application currently re-uploads files for each operation and does not persist users, files, jobs, sessions, or generated patterns.
- Alternatives: Add Render PostgreSQL now, attach persistent storage, or deploy the existing stateless request flow.
- Decision: Deploy the Phase 8 MVP as a stateless Render Web Service without PostgreSQL or a persistent disk.
- Rationale: A database would add cost, migrations, credentials, backup obligations, and failure modes without serving a current requirement. Render's ephemeral filesystem is sufficient because uploaded data exists only for the lifetime of a request.
- Impact: The service can scale only within the in-memory request limits and cannot resume jobs or retain history. A database becomes required when authentication, saved projects, audit history, queued work, or persistent file metadata is introduced.

## 2026-06-24 - Use Blueprint and file-based deployment configuration

- Context: Phase 8 must be repeatable rather than relying on undocumented dashboard clicks.
- Alternatives: Configure Render and Vercel entirely through their dashboards, deploy both components on one platform, or version the supported configuration files.
- Decision: Add a root `render.yaml` for the Django API and `frontend/vercel.json` for the Vite frontend.
- Rationale: Versioned configuration makes build commands, health checks, runtime entrypoints, SPA routing, and non-secret defaults reviewable and reproducible.
- Impact: Account authorization, public URL creation, and secret entry remain external platform actions. Production URLs and CORS values must be recorded after the first deploy.
