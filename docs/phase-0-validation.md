# Phase 0 Validation Checklist

Phase 0 goal: convert the PDF brief into a clear, explainable, repeatable, and verifiable development plan.

## Deliverables

- [x] Project README skeleton exists.
- [x] `.env.example` exists.
- [x] Requirements and scope document exists.
- [x] Architecture document exists.
- [x] API sketch exists.
- [x] Decision log exists.
- [x] MVP scope is separated from optional enhancements.
- [x] Open questions are recorded.

## Explainability Checks

- [x] The project goal can be explained in one paragraph.
- [x] The core user flow is documented.
- [x] Backend module responsibilities are documented.
- [x] Frontend module responsibilities are documented.
- [x] LLM integration strategy is documented.
- [x] The reason for starting with a mock LLM is documented.

## Repeatability Checks

- [x] Future local development steps have a placeholder in README.
- [x] Environment variables have a template in `.env.example`.
- [x] Planned project structure is documented.
- [x] API contracts are documented before implementation.

## Verifiability Checks

- [x] MVP acceptance criteria are documented.
- [x] API success and error responses are sketched.
- [x] Phase boundaries are clear.
- [x] Optional features are not mixed into MVP acceptance.

## Remaining Before Phase 1

- [x] Confirm backend package manager: `requirements.txt`.
- [x] Confirm Python version: Python 3.12.
- [x] Confirm frontend scaffold: Vite React TypeScript template.
- [x] Confirm whether TypeScript will be used in React.
- [x] Confirm the initial deployment target: frontend on Vercel, backend on Render.
- [x] Confirm whether export-to-file is MVP or optional: CSV export is MVP-final; Excel export is optional.

## Recommended Phase 1 Entry Criteria

Start Phase 1 when:

- The planned repository structure is accepted.
- The backend stack is confirmed as Django + Django Ninja.
- The frontend stack is confirmed as React + Vite.
- The first backend endpoint is agreed: `GET /api/health`.
