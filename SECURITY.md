# Security Policy

## Supported Version

Security fixes currently target the latest `main` branch and the public
deployment.

## Reporting

Use GitHub private vulnerability reporting when it is available for this
repository. If it is unavailable, contact the repository owner through GitHub
before sharing technical details.

Do not publish:

- API keys or deployment secrets;
- private or personal files;
- production request data;
- a working denial-of-service payload;
- account or billing information.

Include the affected endpoint or component, reproduction conditions, expected
impact, and a minimal safe proof of concept.

## Current Security Boundaries

- The API is public and unauthenticated.
- CORS restricts browser origins but is not authentication.
- Uploaded files are processed in memory and not intentionally persisted.
- OpenAI requests use `store=false`.
- Regex execution has no timeout and remains vulnerable to pathological
  backtracking.

The public deployment should be treated as a demonstration service, not as a
processor for confidential or regulated data.
