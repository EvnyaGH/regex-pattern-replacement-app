# Product Scope

## Product Goal

Provide a focused workflow for identifying and replacing text patterns in
tabular files without requiring users to write a regular expression from
scratch.

## Current Release

### File Input

- Accept `.csv` and `.xlsx`.
- Reject unsupported, empty, corrupt, oversized, or over-limit files.
- Return column names, preview rows, total row count, and filename.
- Preserve non-target columns during replacement.

### Pattern Generation

- Accept a natural-language pattern description.
- Accept the selected target column and representative sample values.
- Support deterministic mock generation for offline development.
- Support OpenAI generation through the Responses API.
- Return a Python-compatible regex, explanation, and provider name.
- Validate regex length and compilation before returning it.

### Replacement

- Apply replacement only to the selected column.
- Process every row in the uploaded file.
- Allow an empty replacement to delete matches.
- Return a limited processed preview.
- Return total replacement and affected-row counts for the complete file.

### Interface

- Provide clear loading, success, empty, and error states.
- Keep the interface available after API or rendering failures.
- Reset dependent state when a new file or target column is selected.
- Work on desktop and narrow browser widths.

### Operations

- Provide deterministic automated backend tests.
- Provide strict TypeScript and production-build checks.
- Keep secrets outside source control.
- Support public HTTPS deployment with exact-origin CORS.
- Document local setup, deployment, API behavior, privacy, and limits.

## Quality Attributes

- Service-layer business logic remains testable without HTTP.
- API request and response contracts are typed.
- Client-visible errors use stable codes and corrective messages.
- File processing is stateless and does not persist uploaded content.
- External LLM failures do not become unhandled server errors.
- Production settings are controlled through environment variables.

## Configured Boundaries

Default limits include:

- 5 MB upload size;
- 200 preview rows;
- 100,000 processing rows;
- 1,000-character regex;
- 20 sample values accepted by the backend;
- 20-second OpenAI timeout.

See [Error Handling](error-handling.md) for the complete limit table.

## Not Included

- User accounts or authentication.
- Persistent file or transformation history.
- Processed-file download.
- Multiple-column replacement in one operation.
- Background jobs or streaming large-file processing.
- Spreadsheet formatting preservation.
- Regex execution timeout.
- Automated browser test suite.

## Roadmap

Priorities for the next release:

1. Export processed results as CSV.
2. Add bounded regex execution or a safer engine.
3. Add automated end-to-end browser tests.
4. Support multiple selected columns.
5. Add queued processing for larger files.

## Acceptance Scenarios

### Email Redaction

1. Upload `samples/email_sample.csv`.
2. Select the `Email` column.
3. Generate a regex from `Find email addresses in the Email column`.
4. Replace matches with `REDACTED`.
5. Confirm three replacements and unchanged non-target columns.

### Real LLM Generation

1. Enable the OpenAI provider.
2. Request a pattern for Australian mobile phone numbers.
3. Confirm the response identifies `provider=openai`.
4. Confirm the returned regex compiles locally.

### Production Deployment

1. Load the Vercel application over HTTPS.
2. Confirm the frontend calls the Render `/api` endpoint.
3. Complete preview, generation, and replacement without CORS or mixed-content
   errors.
