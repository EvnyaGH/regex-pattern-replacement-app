# LLM Integration

## Current Status

Phase 7.5 implements two interchangeable regex-generation providers:

- `mock`: deterministic email-only generation for tests and offline development.
- `openai`: real model generation through the OpenAI Responses API.

The provider is selected through `LLM_PROVIDER`. API routes do not import or call the OpenAI SDK directly.

## Provider Contract

Both providers accept:

- natural-language pattern description;
- target column name;
- up to the configured number of sample values.

Both return:

```json
{
  "regex": "Python-compatible regex",
  "explanation": "Short explanation",
  "provider": "mock or openai"
}
```

Every generated regex is checked locally for:

- non-empty content;
- configured length limit;
- successful Python `re.compile`.

## Mock Provider

The mock provider remains the default because automated tests must not require:

- network access;
- API credentials;
- paid model calls;
- nondeterministic model output.

It recognizes email descriptions in English or Chinese and can infer email intent from sample values. Unsupported descriptions return `LLM_GENERATION_FAILED`.

## OpenAI Provider

Implementation:

```text
backend/services/openai_llm.py
```

The provider uses:

- official OpenAI Python SDK;
- Responses API;
- strict JSON Schema Structured Outputs;
- `store=false`;
- configurable model, timeout, retry count, reasoning effort, and output-token limit.

The request sends only:

- the user's description;
- selected column name;
- the small sample list already prepared by the frontend.

The model has no tools and receives instructions to treat all submitted values as untrusted data.

## Structured Output

The response schema requires exactly:

```json
{
  "regex": "string",
  "explanation": "string"
}
```

Additional properties are rejected by the API schema. The backend still parses and validates the result because external responses must not bypass local checks.

## Configuration

Offline/default mode:

```text
LLM_PROVIDER=mock
```

Real OpenAI mode:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=<secret>
LLM_MODEL=gpt-5.5
LLM_TIMEOUT_SECONDS=20
LLM_MAX_RETRIES=1
LLM_MAX_OUTPUT_TOKENS=2000
LLM_REASONING_EFFORT=low
```

`OPENAI_API_KEY` must be configured in the process or deployment secret manager. It must not be committed to Git or written to screenshots, logs, README examples, or demo recordings.

## Failure Handling

| Failure | Application code | HTTP |
|---|---|---:|
| Missing key/model | `LLM_CONFIGURATION_ERROR` | 503 |
| Invalid credentials or model access | `LLM_AUTHENTICATION_FAILED` | 503 |
| Rate limit | `LLM_RATE_LIMITED` | 429 |
| Timeout | `LLM_TIMEOUT` | 504 |
| Connection failure | `LLM_CONNECTION_FAILED` | 502 |
| Other provider status failure | `LLM_GENERATION_FAILED` | 502 |
| Model refusal | `LLM_REFUSED` | 422 |
| Incomplete response | `LLM_INCOMPLETE_RESPONSE` | 502 |
| Invalid structured response | `LLM_INVALID_RESPONSE` | 502 |
| Invalid generated regex | `INVALID_GENERATED_REGEX` | 400 |

These failures return the same structured error contract as the rest of the API and do not produce an unhandled 500.

## Automated Tests

OpenAI tests use fake clients and synthetic SDK exceptions. They verify:

- strict schema configuration;
- `store=false`;
- model and reasoning settings;
- successful structured parsing;
- missing-key handling;
- timeout, connection, authentication, rate-limit, and status errors;
- refusal and incomplete responses;
- API provider selection;
- local rejection of invalid generated regex.

No automated test sends a real OpenAI request.

Reasoning tokens count toward `LLM_MAX_OUTPUT_TOKENS`. A value that is too low
can produce an `incomplete` response before any visible JSON is generated.
The default of 2000 keeps the request bounded while leaving room for low-effort
reasoning. Increase it deliberately if the smoke test reports
`reason=max_output_tokens`.

## Real API Smoke Test

This command makes one real API call and may incur cost:

```powershell
$env:LLM_PROVIDER = "openai"
$env:OPENAI_API_KEY = "<your key>"
$env:LLM_MODEL = "gpt-5.5"

Set-Location backend
& "$env:TEMP\rrapp-venv-phase5\Scripts\python.exe" .\scripts\openai_smoke_test.py
```

Expected output includes:

```text
provider=openai
regex=...
explanation=...
```

After testing, remove the key from the current process:

```powershell
Remove-Item Env:OPENAI_API_KEY
```

## Security Limits

- Sample values can contain sensitive data; only a small sample is sent.
- `store=false` is set, but external API use must still be disclosed to users if this becomes a public product.
- Regex length and compilation checks do not fully prevent catastrophic backtracking.
- Editable or model-generated regex should receive stronger ReDoS protection before production use.
