from __future__ import annotations

from typing import Any

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from services.file_parser import (
    dataframe_to_rows,
    parse_uploaded_file,
    validate_preview_limit,
)
from services.replacement import RegexReplacementError, replace_matches


def process_uploaded_file(
    uploaded_file: UploadedFile,
    target_column: str,
    regex: str,
    replacement: str,
    preview_limit: int = 50,
) -> dict[str, Any]:
    validate_preview_limit(preview_limit)
    filename, dataframe = parse_uploaded_file(uploaded_file)
    row_count = int(len(dataframe.index))
    if row_count > settings.MAX_PROCESS_ROWS:
        raise RegexReplacementError(
            code="TOO_MANY_ROWS",
            message="The uploaded file contains more rows than the configured processing limit.",
            details={"max_rows": settings.MAX_PROCESS_ROWS},
        )

    columns = [str(column) for column in dataframe.columns]
    all_rows = dataframe_to_rows(dataframe)
    result = replace_matches(
        columns=columns,
        rows=all_rows,
        target_column=target_column,
        regex=regex,
        replacement=replacement,
    )

    return {
        "filename": filename,
        "columns": columns,
        "rows": result["rows"][:preview_limit],
        "row_count": row_count,
        "preview_limit": preview_limit,
        "replacement_count": result["replacement_count"],
        "affected_row_count": result["affected_row_count"],
    }
