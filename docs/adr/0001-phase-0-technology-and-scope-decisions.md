# ADR 0001: Phase 0 Technology and MVP Scope Decisions

## Status

Accepted

## Date

2026-06-24

## Context

Before entering Phase 1, three project choices must be fixed so the implementation can stay explainable, repeatable, and easy for reviewers to run:

1. Whether the React frontend should use TypeScript.
2. Whether backend dependencies should be managed with `requirements.txt`, Poetry, or uv.
3. Whether exporting processed CSV should be part of the MVP or treated as an optional enhancement.

The project is a technical assessment application, so the decision criteria are:

- Low reviewer setup friction.
- Clear type and API contracts.
- Reliable local reproduction.
- Simple deployment path.
- Avoiding premature scope expansion before the core PDF flow works.

## Research Summary

### React and TypeScript

Official React documentation describes TypeScript as a common way to add type definitions to JavaScript codebases and notes that TypeScript supports JSX. It also documents typing React component props, hooks, events, and state shapes.

Official Vite documentation supports scaffolding a React TypeScript app directly through the `react-ts` template.

Implication for this project:

- The frontend will consume structured API responses from Django Ninja.
- The app will have several UI states: idle, uploading, preview loaded, regex generated, replacing, success, and error.
- TypeScript can make those API contracts and UI states more explicit.
- The extra overhead is acceptable because the frontend scope is small.

### Backend dependency management

Official pip documentation defines requirements files as lists of items to be installed by pip, commonly named `requirements.txt`.

Poetry documentation shows stronger project and dependency management through `pyproject.toml`, `poetry.lock`, virtual environment handling, and reproducible installs when the lock file is committed.

uv documentation provides modern project dependency management and lockfile-oriented workflows, but it introduces another tool that reviewers and deployment platforms must have or install.

Implication for this project:

- This project is an application demo, not a Python package to publish.
- The backend dependency set is expected to be small: Django, Django Ninja, pandas, openpyxl, CORS support, testing tools, and possibly an LLM SDK.
- Many Python deployment platforms understand `requirements.txt` with minimal configuration.
- Poetry or uv would improve lockfile workflows, but add setup concepts that are not necessary for the MVP.

### CSV export scope

The PDF requires displaying processed data, source code, README, public deployment, and demo video. It does not explicitly require exporting the processed file.

However, pandas officially supports writing a DataFrame to CSV through `DataFrame.to_csv`, and the implementation cost is low once processed rows already exist. CSV export also improves the user story because users normally expect processed tabular data to be downloadable.

Implication for this project:

- Export is useful and easy, but it should not delay the core flow.
- The core flow remains: upload -> preview -> generate regex -> replace -> display result.
- CSV export should be implemented only after that core flow is complete and tested.
- Excel export should remain optional because preserving workbook formatting is outside the MVP.

## Decision

### Decision 1: Use TypeScript for React

The frontend will use React with TypeScript, scaffolded with Vite's `react-ts` template.

Planned frontend command:

```bash
npm create vite@latest frontend -- --template react-ts
```

### Decision 2: Use `requirements.txt` for backend dependencies in the MVP

The backend will use a plain `requirements.txt` file for Phase 1 through MVP delivery.

Poetry and uv will not be required for reviewers or deployment.

Dependencies should be pinned or bounded deliberately once the first working backend is created.

Expected initial backend files:

```text
backend/
  requirements.txt
  manage.py
  ...
```

### Decision 3: Include processed CSV export as an MVP-final feature, not a core-flow blocker

CSV export will be included in the MVP only after the core replacement flow is working.

This means:

- The first MVP acceptance path does not depend on export.
- A lightweight `Download CSV` feature should be added before final submission if time permits.
- Excel export remains optional.
- Large-file export remains optional.

## Alternatives Considered

## Alternative 1: React with JavaScript only

Pros:

- Slightly faster for quick prototyping.
- Lower syntax overhead if the developer is less familiar with TypeScript.

Cons:

- API response shapes are less explicit.
- UI state transitions are easier to misuse.
- Refactors across frontend services and components are riskier.

Reason rejected:

- The project is small enough that TypeScript overhead is manageable, and typed API contracts help explainability and maintainability.

## Alternative 2: Poetry for backend dependency management

Pros:

- Strong dependency locking through `poetry.lock`.
- Good virtual environment workflow.
- Clear project metadata in `pyproject.toml`.

Cons:

- Requires reviewers and deployment environments to understand Poetry.
- Adds commands and packaging concepts that are not central to the assessment.
- Some platforms require extra configuration compared with `requirements.txt`.

Reason rejected for MVP:

- The assessment values easy setup and deployment. `requirements.txt` is simpler and sufficient for this backend.

## Alternative 3: uv for backend dependency management

Pros:

- Fast modern dependency management.
- Lockfile-based reproducibility.
- Good long-term project workflow.

Cons:

- Requires another tool to be installed or documented.
- May be less familiar to reviewers than pip and `requirements.txt`.
- Adds process choices that are not necessary for the first MVP.

Reason rejected for MVP:

- uv is technically attractive, but the MVP should minimize external tooling requirements.

## Alternative 4: Treat CSV export as purely optional

Pros:

- Keeps the MVP narrower.
- Avoids adding one more endpoint and frontend action.

Cons:

- Users cannot take the processed result away from the app.
- Demo feels less complete for a data-processing tool.
- Implementation cost is low after replacement output already exists.

Reason partially rejected:

- CSV export should be included near the end of MVP delivery if the core flow is stable, but it must not block earlier milestones.

## Consequences

### Positive Consequences

- Frontend API contracts and UI states will be more explicit through TypeScript.
- Backend setup remains easy to explain with standard pip commands.
- Deployment should be simpler because `requirements.txt` is widely recognized.
- CSV export gives the final demo a more complete data-tool workflow.

### Negative Consequences

- TypeScript adds a small learning and typing overhead.
- `requirements.txt` does not provide the same lockfile semantics as Poetry or uv.
- CSV export adds one extra endpoint or frontend utility near the end of MVP.

### Mitigations

- Keep TypeScript types practical and close to API shapes; avoid over-engineering generic types.
- Pin important backend dependencies after Phase 1 scaffolding.
- Keep CSV export simple: processed rows -> CSV string/file; no Excel formatting preservation.
- Revisit Poetry or uv only if dependency complexity grows materially.

## Implementation Notes

### Frontend

- Scaffold with `react-ts`.
- Define API response types in `frontend/src/types/api.ts`.
- Use discriminated unions for request states if the state logic becomes complex.

### Backend

- Use `backend/requirements.txt`.
- Include installation instructions:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

- Keep optional local tooling outside the required reviewer path.

### CSV Export

Possible endpoint:

```text
POST /api/files/export
```

Expected request:

```json
{
  "columns": ["ID", "Name", "Email"],
  "rows": [
    {"ID": 1, "Name": "John Doe", "Email": "REDACTED"}
  ],
  "format": "csv"
}
```

Expected behavior:

- Return a downloadable CSV response.
- Use UTF-8 encoding.
- Do not include DataFrame index.
- Keep Excel export out of MVP unless time remains after deployment and demo video.

## Documentation Updates Required

After this ADR is accepted:

- Update `docs/requirements.md` so CSV export is listed as MVP-final rather than purely optional.
- Update `docs/architecture.md` to mention TypeScript frontend types and `requirements.txt` backend dependency management.
- Update `docs/api.md` when the export endpoint is actually implemented.
- Update `docs/phase-0-validation.md` to mark these three choices as resolved.
- Optionally append a short summary to `docs/decision-log.md`.

## References

- React official documentation, `Using TypeScript`: https://react.dev/learn/typescript
- Vite official documentation, `Scaffolding Your First Vite Project`: https://vite.dev/guide/
- pip official documentation, `Requirements File Format`: https://pip.pypa.io/en/stable/reference/requirements-file-format/
- Poetry official documentation, `Basic usage`: https://python-poetry.org/docs/basic-usage/
- uv official documentation, `Managing dependencies`: https://docs.astral.sh/uv/concepts/projects/dependencies/
- pandas official documentation, `DataFrame.to_csv`: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
