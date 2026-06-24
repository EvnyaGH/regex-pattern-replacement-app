# Architecture

## Architecture Goal

The application should keep API routing, business logic, LLM integration, and UI state separate enough that each part can be tested and explained independently.

The core design principle is:

> API routes coordinate requests and responses; service modules perform file parsing, regex generation, and replacement logic.

## High-Level Components

```text
User Browser
  |
  v
React Frontend
  |
  v
Django Ninja API
  |
  +--> File Parsing Service
  |
  +--> Regex Generation Service
  |      |
  |      +--> Mock LLM Service
  |      |
  |      +--> Real LLM Service
  |
  +--> Replacement Service
```

## Data Flow

```text
1. User uploads CSV/Excel file
2. Frontend sends file to backend preview API
3. Backend parses file into columns and rows
4. Frontend renders preview table
5. User selects target column and enters natural language description
6. Frontend requests regex generation
7. Backend regex service returns regex and explanation
8. User enters replacement value and confirms replacement
9. Frontend re-uploads the original file with column, regex, and replacement value
10. Backend parses the complete file and applies regex to every row
11. Backend returns a limited processed preview and full-file replacement statistics
12. Frontend renders processed output
```

## Planned Backend Structure

```text
backend/
  manage.py
  requirements.txt
  config/
    settings.py
    urls.py
  api/
    router.py
    file_routes.py
    regex_routes.py
    health_routes.py
  schemas/
    file_schemas.py
    regex_schemas.py
    error_schemas.py
  services/
    file_parser.py
    regex_generator.py
    replacement.py
    llm_client.py
  tests/
    test_file_parser.py
    test_regex_generator.py
    test_replacement.py
    test_api_flow.py
```

## Planned Frontend Structure

```text
frontend/
  package.json
  src/
    main.tsx
    App.tsx
    components/
      FileUpload.tsx
      DataPreviewTable.tsx
      RegexInputPanel.tsx
      ReplacementPanel.tsx
      ResultTable.tsx
      ErrorMessage.tsx
    services/
      apiClient.ts
      fileApi.ts
      regexApi.ts
    types/
      api.ts
```

## Module Responsibilities

### React Frontend

- Owns user interactions.
- Stores current UI state.
- Sends files and form inputs to the backend.
- Displays preview data, generated regex, processed output, loading state, and errors.
- Uses TypeScript to define API response types and UI request states.
- Implementation status: Phase 5 implemented under `frontend/`.

### Django Ninja API

- Defines HTTP endpoints.
- Validates request and response schemas.
- Calls service-layer functions.
- Converts service errors into consistent API responses.
- Uses `requirements.txt` for MVP backend dependency installation.

### File Parsing Service

- Accepts uploaded CSV/Excel files.
- Validates file type and file size.
- Parses data into columns and rows.
- Applies preview row limits.
- Implementation status: Phase 2 implemented in `backend/services/file_parser.py`.

### File Processing Service

- Reuses the same upload validation and parsing rules as preview.
- Applies replacement to all parsed rows.
- Limits only the processed rows returned to the frontend.
- Keeps processing stateless by re-uploading the original file.
- Implementation status: Phase 6 implemented in `backend/services/file_processor.py`.

### Regex Generation Service

- Accepts natural language description, target column, and optional sample values.
- Calls mock or real LLM provider.
- Validates that generated regex can compile.
- Returns regex and explanation.
- Implementation status: `backend/services/regex_generator.py` selects the mock or OpenAI provider and validates every generated regex.

### Replacement Service

- Accepts rows, target column, regex, and replacement value.
- Applies regex replacement only to the selected column.
- Returns processed rows and statistics.
- Implementation status: Phase 4 implemented in `backend/services/replacement.py`.

### LLM Client

- Encapsulates external LLM API calls.
- Reads API configuration from environment variables.
- Makes the implementation replaceable.
- Uses the OpenAI Responses API with strict JSON Schema Structured Outputs.
- Maps provider failures to stable application error codes.
- Implementation status: Phase 7.5 implemented in `backend/services/openai_llm.py`.

## Error Handling Strategy

Errors should be returned in a consistent shape:

```json
{
  "error": {
    "code": "INVALID_REGEX",
    "message": "The generated regex could not be compiled.",
    "details": {}
  }
}
```

Expected error categories:

- Invalid file type.
- Empty file.
- File parsing failure.
- Missing target column.
- Empty natural language description.
- LLM generation failure.
- Invalid regex.
- No matches found.
- Unexpected server error.

## Initial Design Decisions

- Use Django Ninja instead of plain Django views to keep typed request/response contracts.
- Use a service layer so parsing, LLM, and replacement logic can be tested without HTTP.
- Start with a mock LLM to make the project reproducible before real API credentials exist.
- Return generated regex to the user before replacement for transparency.
- Avoid persistent file storage in the MVP unless a later phase requires it.

## Deployment Architecture

```text
Browser
  |
  | HTTPS
  v
Vercel static frontend
  |
  | HTTPS JSON and multipart requests
  v
Render Django API
  |
  | HTTPS structured-output request
  v
OpenAI Responses API
```

The Render service is stateless. Uploaded files are parsed and processed in
memory during the request and are not persisted. This keeps the Phase 8
deployment aligned with the existing service boundaries and avoids introducing
a database before the application has persistent domain data.
