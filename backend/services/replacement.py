from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

from django.conf import settings


@dataclass
class RegexReplacementError(Exception):
    code: str
    message: str
    status_code: int = 400
    details: dict[str, Any] = field(default_factory=dict)


def replace_matches(
    columns: list[str],
    rows: list[dict[str, Any]],
    target_column: str,
    regex: str,
    replacement: str,
) -> dict[str, Any]:
    column = target_column.strip()
    if not column:
        raise RegexReplacementError(
            code="MISSING_TARGET_COLUMN",
            message="Target column is required.",
        )

    if len(column) > settings.MAX_TARGET_COLUMN_LENGTH:
        raise RegexReplacementError(
            code="TARGET_COLUMN_TOO_LONG",
            message="Target column name exceeds the configured length limit.",
            details={"max_length": settings.MAX_TARGET_COLUMN_LENGTH},
        )

    if not rows:
        raise RegexReplacementError(
            code="NO_ROWS",
            message="At least one row is required for replacement.",
        )

    if len(rows) > settings.MAX_PROCESS_ROWS:
        raise RegexReplacementError(
            code="TOO_MANY_ROWS",
            message="The request contains more rows than the configured processing limit.",
            details={"max_rows": settings.MAX_PROCESS_ROWS},
        )

    if column not in columns:
        raise RegexReplacementError(
            code="TARGET_COLUMN_NOT_FOUND",
            message="Target column does not exist in the provided columns.",
            details={"target_column": column, "columns": columns},
        )

    if len(replacement) > settings.MAX_REPLACEMENT_LENGTH:
        raise RegexReplacementError(
            code="REPLACEMENT_TOO_LONG",
            message="Replacement text exceeds the configured length limit.",
            details={"max_length": settings.MAX_REPLACEMENT_LENGTH},
        )

    pattern = _compile_regex(regex)

    processed_rows: list[dict[str, Any]] = []
    replacement_count = 0
    affected_row_count = 0

    for row in rows:
        processed_row = dict(row)
        value = processed_row.get(column)
        if value is None:
            processed_rows.append(processed_row)
            continue

        text = str(value)
        new_text, count = pattern.subn(replacement, text)
        if count:
            processed_row[column] = new_text
            replacement_count += count
            affected_row_count += 1

        processed_rows.append(processed_row)

    return {
        "columns": columns,
        "rows": processed_rows,
        "replacement_count": replacement_count,
        "affected_row_count": affected_row_count,
    }


def _compile_regex(regex: str) -> re.Pattern[str]:
    if not regex.strip():
        raise RegexReplacementError(
            code="INVALID_REGEX",
            message="Regex is required.",
        )

    if len(regex) > settings.MAX_REGEX_LENGTH:
        raise RegexReplacementError(
            code="REGEX_TOO_LONG",
            message="Regex exceeds the configured length limit.",
            details={"max_length": settings.MAX_REGEX_LENGTH},
        )

    try:
        return re.compile(regex)
    except re.error as exc:
        raise RegexReplacementError(
            code="INVALID_REGEX",
            message="Regex could not be compiled.",
            details={"reason": str(exc)},
        ) from exc
