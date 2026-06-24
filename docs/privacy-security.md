# Privacy and Security

## Data Flow

Uploaded files are sent from the browser to the Django backend for preview and
processing.

- Files are parsed in memory during the request.
- The application does not save uploaded files to a database or persistent
  filesystem.
- The browser retains the selected local file so it can be uploaded again for
  complete processing.
- Processed rows and generated regex remain in browser memory until the page is
  refreshed or replaced by another workflow.

The deployed backend runs on Render. Platform-level request metadata and logs
remain subject to Render's service configuration and policies.

## OpenAI Data

When `LLM_PROVIDER=openai`, the backend sends:

- the natural-language pattern description;
- the selected column name;
- the supplied sample values.

The application sets `store=false` on Responses API requests. This setting does
not replace an independent review of OpenAI's current API data controls,
retention terms, and organizational requirements.

Do not use the public deployment for confidential, regulated, production, or
personally identifying data.

## Public Endpoint Exposure

The production API is publicly reachable and does not require authentication.
Its configured controls include:

- exact-origin browser CORS;
- upload and row limits;
- natural-language, sample, regex, and replacement length limits;
- OpenAI timeout and retry limits;
- structured provider failure handling;
- HTTPS redirect and secure production settings.

CORS is a browser control, not API authentication. Direct non-browser clients
can still call public endpoints.

## Regex Risk

Generated regex is length-limited and compiled before use. Python `re`
execution does not currently have a timeout, so pathological patterns can still
cause excessive CPU use through catastrophic backtracking.

Treat generated regex as untrusted input. A safer execution boundary is a
priority before supporting arbitrary production workloads.

## Secrets

- Keep `OPENAI_API_KEY` and `DJANGO_SECRET_KEY` in deployment secret managers
  or process environment variables.
- Never commit `.env` or paste secrets into issues, logs, screenshots, or demo
  recordings.
- Rotate a key immediately if exposure is suspected.
- Apply OpenAI project budgets and usage alerts to public deployments.

## Reporting Security Issues

Follow [SECURITY.md](../SECURITY.md). Do not include API keys, private files, or
personal data in a public GitHub issue.
