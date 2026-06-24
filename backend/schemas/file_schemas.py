from typing import Any

from ninja import Schema


class FilePreviewResponse(Schema):
    filename: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    preview_limit: int


class FileProcessResponse(FilePreviewResponse):
    replacement_count: int
    affected_row_count: int
