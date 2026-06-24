from __future__ import annotations

import json
import os
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django


def main() -> int:
    django.setup()

    from services.regex_generator import RegexGenerationError, generate_regex

    try:
        result = generate_regex(
            natural_language="Find Australian mobile phone numbers",
            target_column="Phone",
            sample_values=["0412 345 678", "+61 412 345 678"],
            provider="openai",
        )
    except RegexGenerationError as exc:
        print(f"error_code={exc.code}", file=sys.stderr)
        print(f"message={exc.message}", file=sys.stderr)
        if exc.details:
            print(
                f"details={json.dumps(exc.details, ensure_ascii=False)}",
                file=sys.stderr,
            )
        if exc.details.get("reason") == "max_output_tokens":
            print(
                "hint=Increase LLM_MAX_OUTPUT_TOKENS and retry once; 2000 is the project default.",
                file=sys.stderr,
            )
        return 1

    print(f"provider={result['provider']}")
    print(f"regex={result['regex']}")
    print(f"explanation={result['explanation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
