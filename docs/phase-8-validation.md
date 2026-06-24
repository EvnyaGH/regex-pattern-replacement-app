# Phase 8 Validation Checklist

Phase 8 goal: deploy the frontend and backend to public HTTPS endpoints with
production-safe configuration and repeatable instructions.

## Deployment Preparation

- [x] Render Blueprint added.
- [x] Gunicorn production server added.
- [x] WhiteNoise static-file handling added.
- [x] Production secret, debug, host, HTTPS, and cookie settings added.
- [x] Render hostname is added to `ALLOWED_HOSTS` automatically.
- [x] Production CORS and CSRF origins are environment-controlled.
- [x] Vercel Vite configuration added.
- [x] Frontend API base URL remains environment-controlled.
- [x] Real secrets remain excluded from source control.
- [x] Deployment procedure documented.
- [x] No-database deployment decision documented.

## Local Verification

- [x] Backend dependency installation succeeds from `requirements.txt`.
- [x] Backend automated suite passes: 47 tests.
- [x] Django deployment checks pass with only the documented HSTS
  `includeSubDomains` and `preload` warnings retained.
- [x] HTTPS health request passes using production settings.
- [x] Production CORS origin check passes.
- [x] HTTP requests redirect to HTTPS.
- [x] Cross-origin JSON POST passes with production middleware.
- [x] `collectstatic` succeeds.
- [x] Frontend TypeScript and production build pass.

## External Deployment

- [x] Repository published publicly at
  `https://github.com/EvnyaGH/regex-pattern-replacement-app`.
- [x] Render Blueprint applied.
- [x] Render health endpoint publicly returns `{"status":"ok"}` at
  `https://regex-pattern-replacement-api.onrender.com/api/health`.
- [ ] Vercel project deployed from the `frontend` root directory.
- [ ] `VITE_API_BASE_URL` points to the Render `/api` URL.
- [ ] Render CORS origin points to the exact Vercel production origin.
- [ ] Public browser workflow passes using `samples/email_sample.csv`.
- [ ] Public real-OpenAI regex generation passes.
- [ ] Public URLs are added to README.

## Acceptance Status

Deployment preparation is code-complete. Phase 8 is accepted only after the
external deployment checklist is complete and both public URLs are recorded.
