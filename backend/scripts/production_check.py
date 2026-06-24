from __future__ import annotations

import json
import os
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
os.environ["DJANGO_PRODUCTION"] = "true"
os.environ["DJANGO_DEBUG"] = "false"
os.environ["DJANGO_SECRET_KEY"] = (
    "deployment-check-only-9f3d7ac4b6e14d299e3a8803f7f8f9e7"
)
os.environ["DJANGO_ALLOWED_HOSTS"] = "deployment-check.local"
os.environ["CORS_ALLOWED_ORIGINS"] = "https://frontend.example"
os.environ["LLM_PROVIDER"] = "mock"

import django
from django.core.checks import run_checks
from django.test import Client


def main() -> int:
    django.setup()

    allowed_warning_ids = {"security.W005", "security.W021"}
    issues = run_checks(include_deployment_checks=True)
    unexpected_issues = [
        issue for issue in issues if issue.id not in allowed_warning_ids
    ]
    if unexpected_issues:
        for issue in unexpected_issues:
            print(f"{issue.id}: {issue.msg}", file=sys.stderr)
        return 1

    response = Client(HTTP_HOST="deployment-check.local").get(
        "/api/health",
        secure=True,
        HTTP_ORIGIN="https://frontend.example",
    )
    if response.status_code != 200 or response.json() != {"status": "ok"}:
        print(
            f"Production health check failed: status={response.status_code}",
            file=sys.stderr,
        )
        return 1

    if (
        response.headers.get("Access-Control-Allow-Origin")
        != "https://frontend.example"
    ):
        print("Production CORS check failed.", file=sys.stderr)
        return 1

    redirect_response = Client(HTTP_HOST="deployment-check.local").get(
        "/api/health",
    )
    if redirect_response.status_code not in {301, 302}:
        print("HTTP to HTTPS redirect check failed.", file=sys.stderr)
        return 1

    regex_response = Client(HTTP_HOST="deployment-check.local").post(
        "/api/regex/generate",
        data=json.dumps(
            {
                "natural_language": "Find email addresses",
                "target_column": "Email",
                "sample_values": ["person@example.com"],
            }
        ),
        content_type="application/json",
        secure=True,
        HTTP_ORIGIN="https://frontend.example",
    )
    if regex_response.status_code != 200:
        print(
            "Production cross-origin POST check failed: "
            f"status={regex_response.status_code}",
            file=sys.stderr,
        )
        return 1

    print("Django deployment checks passed.")
    print(
        "Documented HSTS warnings retained until a custom domain policy is chosen: "
        "security.W005, security.W021."
    )
    print("HTTPS health endpoint passed.")
    print("Production CORS origin passed.")
    print("HTTP to HTTPS redirect passed.")
    print("Cross-origin API POST passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
