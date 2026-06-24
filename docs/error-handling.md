# Error Handling

## Response Contract

Application and request-validation errors use:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable corrective message.",
    "details": {}
  }
}
```

Django Ninja schema errors are normalized to this contract instead of returning its default `detail` payload.

## Error Matrix

| Scenario | HTTP | Code | Frontend behavior |
|---|---:|---|---|
| Missing or invalid request field | 422 | `REQUEST_VALIDATION_ERROR` | Shows submitted-values error |
| Malformed JSON body | 400 | `INVALID_REQUEST_BODY` | Shows invalid-request error |
| Unsupported extension | 400 | `INVALID_FILE_TYPE` | Prompts for CSV or XLSX |
| Empty file | 400 | `EMPTY_FILE` | Explains that no readable data exists |
| Corrupt CSV/XLSX | 400 | `FILE_PARSE_ERROR` | Explains that parsing failed |
| File over byte limit | 413 | `FILE_TOO_LARGE` | Shows configured-size failure |
| Preview limit invalid | 400 | `INVALID_PREVIEW_LIMIT` | Shows allowed range |
| File over row limit | 400 | `TOO_MANY_ROWS` | Explains processing limit |
| Empty natural-language input | 400 | `EMPTY_DESCRIPTION` | Prompts for a description |
| Description over limit | 400 | `DESCRIPTION_TOO_LONG` | Shows configured limit |
| Too many or oversized samples | 400 | `TOO_MANY_SAMPLE_VALUES` / `SAMPLE_VALUE_TOO_LONG` | Shows generation input error |
| Unsupported mock request | 400 | `LLM_GENERATION_FAILED` | Explains mock limitation |
| OpenAI configuration missing | 503 | `LLM_CONFIGURATION_ERROR` | Explains required backend configuration |
| OpenAI authentication/model access failure | 503 | `LLM_AUTHENTICATION_FAILED` | Shows provider access failure |
| OpenAI rate limit | 429 | `LLM_RATE_LIMITED` | Prompts user to retry later |
| OpenAI timeout | 504 | `LLM_TIMEOUT` | Reports provider timeout |
| OpenAI connection failure | 502 | `LLM_CONNECTION_FAILED` | Reports provider unavailability |
| OpenAI refusal | 422 | `LLM_REFUSED` | Explains that the request was declined |
| OpenAI incomplete/invalid response | 502 | `LLM_INCOMPLETE_RESPONSE` / `LLM_INVALID_RESPONSE` | Reports provider contract failure |
| Missing target column | 400 | `MISSING_TARGET_COLUMN` | Prompts for a column |
| Column absent from data | 400 | `TARGET_COLUMN_NOT_FOUND` | Shows missing-column error |
| Invalid or empty regex | 400 | `INVALID_REGEX` | Shows invalid-regex error |
| Regex over length limit | 400 | `REGEX_TOO_LONG` | Shows configured limit |
| Replacement over limit | 400 | `REPLACEMENT_TOO_LONG` | Shows configured limit |
| No rows supplied | 400 | `NO_ROWS` | Explains that data is required |
| No regex matches | 200 | zero counts | Displays successful zero-result state |
| Backend unavailable | Client | `NETWORK_ERROR` | Keeps UI mounted and shows retry guidance |
| Backend timeout | Client | `REQUEST_TIMEOUT` | Keeps UI mounted and reports timeout |
| Non-JSON success response | Client | `INVALID_RESPONSE` | Reports backend contract failure |
| Unexpected render failure | Client | Error boundary | Displays reload action instead of blank page |

## Configured Limits

| Environment variable | Default |
|---|---:|
| `MAX_UPLOAD_BYTES` | 5 MB |
| `MAX_PREVIEW_ROWS` | 200 |
| `MAX_PROCESS_ROWS` | 100,000 |
| `MAX_REGEX_LENGTH` | 1,000 characters |
| `MAX_REPLACEMENT_LENGTH` | 10,000 characters |
| `MAX_NATURAL_LANGUAGE_LENGTH` | 2,000 characters |
| `MAX_TARGET_COLUMN_LENGTH` | 255 characters |
| `MAX_SAMPLE_VALUES` | 20 |
| `MAX_SAMPLE_VALUE_LENGTH` | 1,000 characters |
| `VITE_API_TIMEOUT_MS` | 15,000 ms |
| `LLM_TIMEOUT_SECONDS` | 20 seconds |
| `LLM_MAX_RETRIES` | 1 |
| `LLM_MAX_OUTPUT_TOKENS` | 2000 |
| `LLM_REASONING_EFFORT` | `low` |

## Known Residual Risk

Regex is compiled and length-limited, but Python `re` execution does not have a timeout. OpenAI-generated regex broadens the possible pattern surface, so stronger ReDoS protection is required before treating arbitrary generated patterns as production-safe.
