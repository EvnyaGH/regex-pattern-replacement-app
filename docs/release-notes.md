# Release Notes

## v0.1.0 - 2026-06-24

Initial public release.

### Application

- CSV and XLSX upload with tabular preview.
- Target-column selection.
- Natural-language regex generation.
- Deterministic mock provider for local development and tests.
- OpenAI Responses API provider with strict Structured Outputs.
- Full-file, column-scoped replacement with processed preview and statistics.
- Responsive React and TypeScript interface.
- Structured backend and frontend error handling.

### Operations

- Vercel frontend deployment.
- Render Django API deployment.
- Exact-origin production CORS.
- HTTPS and secure Django production settings.
- Versioned Render and Vercel deployment configuration.
- Stateless processing with no persistent database.

### Validation

- 48 backend tests.
- Strict TypeScript compilation.
- Vite production build.
- Django production checks.
- Public health, CORS, upload, replacement, and real OpenAI verification.

### Known Limitations

- No processed-file export.
- No regex execution timeout.
- No authentication or persistent history.
- One target column per operation.
- No automated browser test suite.
- Render free-tier cold starts can delay the first request.
