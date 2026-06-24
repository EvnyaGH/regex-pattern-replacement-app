from pydantic import Field
from ninja import Schema
from typing import Any


class RegexGenerateRequest(Schema):
    natural_language: str
    target_column: str
    sample_values: list[str] = Field(default_factory=list)


class RegexGenerateResponse(Schema):
    regex: str
    explanation: str
    provider: str


class RegexReplaceRequest(Schema):
    columns: list[str]
    rows: list[dict[str, Any]]
    target_column: str
    regex: str
    replacement: str = ""


class RegexReplaceResponse(Schema):
    columns: list[str]
    rows: list[dict[str, Any]]
    replacement_count: int
    affected_row_count: int
