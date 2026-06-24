from __future__ import annotations

import os
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
from django.core.management import call_command


def main() -> int:
    for path in BACKEND_DIR.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        compile(path.read_text(encoding="utf-8"), str(path), "exec")

    django.setup()
    call_command("check")
    call_command("test", verbosity=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
