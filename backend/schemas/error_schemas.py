from typing import Any

from pydantic import Field
from ninja import Schema


class ErrorDetail(Schema):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(Schema):
    error: ErrorDetail
