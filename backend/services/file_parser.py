from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from io import BytesIO
from pathlib import Path
from typing import Any

import pandas as pd
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile


SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


@dataclass
class FilePreviewError(Exception):
    code: str
    message: str
    status_code: int = 400
    details: dict[str, Any] = field(default_factory=dict)


def build_file_preview(uploaded_file: UploadedFile, preview_limit: int = 50) -> dict[str, Any]:
    validate_preview_limit(preview_limit)
    filename, dataframe = parse_uploaded_file(uploaded_file)
    columns = [str(column) for column in dataframe.columns]
    rows = dataframe_to_rows(dataframe.head(preview_limit))

    return {
        "filename": filename,
        "columns": columns,
        "rows": rows,
        "row_count": int(len(dataframe.index)),
        "preview_limit": preview_limit,
    }


def validate_preview_limit(preview_limit: int) -> None:
    if preview_limit < 1 or preview_limit > settings.MAX_PREVIEW_ROWS:
        raise FilePreviewError(
            code="INVALID_PREVIEW_LIMIT",
            message=f"preview_limit must be between 1 and {settings.MAX_PREVIEW_ROWS}.",
            details={"max_preview_rows": settings.MAX_PREVIEW_ROWS},
        )


def parse_uploaded_file(uploaded_file: UploadedFile) -> tuple[str, pd.DataFrame]:
    filename = uploaded_file.name or ""
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise FilePreviewError(
            code="INVALID_FILE_TYPE",
            message="Only .csv and .xlsx files are supported.",
            details={"supported_extensions": sorted(SUPPORTED_EXTENSIONS)},
        )

    if uploaded_file.size == 0:
        raise FilePreviewError(
            code="EMPTY_FILE",
            message="The uploaded file is empty.",
        )

    if uploaded_file.size > settings.MAX_UPLOAD_BYTES:
        raise FilePreviewError(
            code="FILE_TOO_LARGE",
            message="The uploaded file exceeds the configured size limit.",
            status_code=413,
            details={"max_upload_bytes": settings.MAX_UPLOAD_BYTES},
        )

    content = uploaded_file.read()
    if not content:
        raise FilePreviewError(
            code="EMPTY_FILE",
            message="The uploaded file is empty.",
        )

    try:
        dataframe = _read_dataframe(content, extension)
    except pd.errors.EmptyDataError as exc:
        raise FilePreviewError(
            code="EMPTY_FILE",
            message="The uploaded file has no readable data.",
        ) from exc
    except Exception as exc:
        raise FilePreviewError(
            code="FILE_PARSE_ERROR",
            message="The uploaded file could not be parsed.",
            details={"reason": str(exc)},
        ) from exc

    columns = [str(column) for column in dataframe.columns]
    if not columns:
        raise FilePreviewError(
            code="EMPTY_FILE",
            message="The uploaded file has no readable columns.",
        )

    return filename, dataframe


def dataframe_to_rows(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {str(column): _json_safe(value) for column, value in row.items()}
        for row in dataframe.to_dict(orient="records")
    ]


def _read_dataframe(content: bytes, extension: str) -> pd.DataFrame:
    buffer = BytesIO(content)
    if extension == ".csv":
        return pd.read_csv(buffer)
    if extension == ".xlsx":
        return pd.read_excel(buffer, engine="openpyxl")
    raise ValueError(f"Unsupported extension: {extension}")


def _json_safe(value: Any) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value
