# Requirements and Scope

## Source Brief

The project is based on the PDF task brief titled `Web Application for Regex Pattern Matching and Replacement`.

The brief asks for a Django and React web application that allows users to:

- Upload CSV or Excel files.
- Identify patterns in text columns using natural language input.
- Use an LLM to convert natural language into a regex pattern.
- Replace matched patterns.
- Display processed data.
- Submit source code through GitHub.
- Provide a README.
- Deploy the final application to a publicly accessible environment.
- Include a demo video embedded in the GitHub README.

## MVP Functional Requirements

### File Upload

- The user can upload a `.csv` file.
- The user can upload a `.xlsx` file.
- The backend parses the uploaded file.
- The frontend displays a tabular preview.
- The preview includes column names and row data.

### Pattern Generation

- The user can choose a target column.
- The user can describe the pattern to find in natural language.
- The backend can generate a regex pattern from the natural language description.
- The backend supports deterministic mock generation and real OpenAI generation selected by environment configuration.
- The generated regex is returned to the frontend for review.

### Replacement

- The user can specify a replacement value.
- The backend applies the regex to the selected text column.
- The backend returns processed rows.
- The backend returns replacement statistics, including replacement count and affected row count.

### Display

- The frontend displays uploaded preview data.
- The frontend displays generated regex output.
- The frontend displays processed output data.
- The frontend displays clear loading and error states.

### CSV Export

- After the core replacement flow works, the user can download processed data as CSV.
- CSV export is an MVP-final feature, not a blocker for the first end-to-end replacement flow.
- Excel export remains optional.

### Delivery

- The project includes a README.
- The project includes setup instructions.
- The project includes test instructions.
- The project includes a public deployment URL.
- The project includes a demo video link or embed.

## Non-Functional Requirements

- Code should be clean, maintainable, and documented where needed.
- Backend business logic should be testable outside API route handlers.
- API responses should be predictable and typed.
- Error handling should be clear for users and developers.
- Environment variables should be documented.
- Real secrets must not be committed.

## MVP Acceptance Criteria

The MVP is accepted when:

- A user can upload a sample CSV containing an `Email` column.
- The frontend displays the uploaded table.
- The user can enter: `Find email addresses in the Email column and replace them with 'REDACTED'.`
- The system generates a valid email regex.
- The system replaces all email addresses in the selected column with `REDACTED`.
- The processed table is displayed.
- The processed table can be downloaded as CSV before final submission, after the core flow is stable.
- The same flow can be reproduced from README instructions.

## Explicit Non-Scope for MVP

The following are not required for the first MVP:

- User authentication.
- Persistent database storage for uploaded files.
- Multi-user collaboration.
- Advanced spreadsheet formatting preservation.
- Full large-file streaming architecture.
- Background job queue.
- Multiple LLM providers.
- Complex regex safety sandbox beyond compile validation and controlled replacement.

## Optional Enhancements

Optional enhancements should be considered only after the MVP works end to end:

- Export processed data as Excel.
- Support multiple target columns.
- Support large files with preview limits and chunked processing.
- Add two extra LLM-powered data transformations, such as phone normalization or date extraction.
- Add frontend automated tests.
- Add richer deployment monitoring.

## Open Questions

- Should the user be allowed to edit the generated regex before replacement?

Resolved:

- Hosted-demo upload limit defaults to 5 MB.
- CSV download remains an MVP-final feature.
- Backend deployment target is Render and frontend target is Vercel.
- The real LLM provider is OpenAI through the Responses API; mock remains available for tests.
