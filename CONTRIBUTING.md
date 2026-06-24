# Contributing

## Development Setup

Follow [Local Development](docs/local-development.md).

## Change Scope

- Keep API routes thin and place domain behavior in `backend/services/`.
- Keep frontend API behavior in `frontend/src/services/apiClient.ts`.
- Update API, architecture, error, deployment, or privacy documentation when a
  change affects those contracts.
- Do not commit secrets, generated environments, dependency directories,
  database files, or build output.

## Branch and Commit Workflow

1. Create a focused branch from `main`.
2. Make one coherent change.
3. Run the relevant checks.
4. Commit with a concise description of the outcome.
5. Open a pull request describing behavior, risk, and validation.

## Required Checks

Backend changes:

```powershell
Set-Location .\backend
& "..\.venv\Scripts\python.exe" .\scripts\quality_check.py
& "..\.venv\Scripts\python.exe" .\scripts\production_check.py
```

Frontend changes:

```powershell
Set-Location .\frontend
npm.cmd run check
```

Documentation-only changes should still pass `git diff --check` and should be
checked for stale URLs, commands, limits, and feature claims.

## Pull Requests

Include:

- the user-visible or developer-visible behavior changed;
- the reason for the change;
- relevant security, privacy, compatibility, or deployment impact;
- tests and manual checks performed;
- screenshots only when they do not expose private data or credentials.

## Security

Do not open a public issue for a vulnerability that exposes secrets, private
data, or a practical abuse path. Follow [SECURITY.md](SECURITY.md).
