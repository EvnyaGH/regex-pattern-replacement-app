# Phase 7.5 Validation Checklist

Phase 7.5 goal: add a real OpenAI regex-generation provider without sacrificing deterministic offline tests.

## Deliverables

- [x] Official OpenAI Python SDK dependency.
- [x] `mock` and `openai` provider selection.
- [x] Responses API integration.
- [x] Strict JSON Schema Structured Outputs.
- [x] `store=false`.
- [x] Configurable model, timeout, retries, reasoning effort, and output limit.
- [x] Missing-key and provider-error handling.
- [x] Local regex length and compilation validation.
- [x] Fake-client automated tests with no paid calls.
- [x] Real API smoke-test script.
- [x] Frontend provider display.
- [x] README, LLM guide, API docs, error matrix, ADR, and `.env.example` updated.

## Configuration

Default deterministic mode:

```text
LLM_PROVIDER=mock
```

Real provider mode:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=<secret>
LLM_MODEL=gpt-5.5
```

The key must exist only in the process environment or deployment secret manager.

## Automated Validation

Backend:

```powershell
Set-Location backend
& "$env:TEMP\rrapp-venv-phase5\Scripts\python.exe" .\scripts\quality_check.py
```

Result:

```text
OpenAI SDK: 2.43.0
Dependency check: passed
Django system check: passed
Tests: 47 passed
```

Frontend:

```powershell
Set-Location frontend
npm.cmd run check
```

Result:

```text
Strict TypeScript check: passed
Vite production build: passed
```

## Provider Failure Coverage

- [x] Missing API key.
- [x] Unsupported provider.
- [x] Authentication or model permission failure.
- [x] Rate limit.
- [x] Timeout.
- [x] Connection failure.
- [x] Other OpenAI status failure.
- [x] Model refusal.
- [x] Incomplete response.
- [x] Invalid structured output.
- [x] Invalid generated regex.

## Real API Verification

- [x] Run `backend/scripts/openai_smoke_test.py` with a valid user-supplied `OPENAI_API_KEY`.

Verified on 2026-06-24 with the OpenAI provider:

```text
provider=openai
regex=(?<!\d)(?:04\d{2} ?\d{3} ?\d{3}|\+61 ?4\d{2} ?\d{3} ?\d{3})(?!\d)
explanation=Matches Australian mobile numbers in local or international format.
```

The complete explanation included examples for `0412 345 678` and
`+61 412 345 678`. The returned regex is Python-compatible and passed the
backend's local compilation validation.

This verification is intentionally excluded from automated tests because it
requires a secret, network access, and a potentially billable call. Stage 7.5
now meets all acceptance criteria.
