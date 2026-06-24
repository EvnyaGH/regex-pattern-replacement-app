from ninja import Router

from schemas.error_schemas import ErrorResponse
from schemas.regex_schemas import (
    RegexGenerateRequest,
    RegexGenerateResponse,
    RegexReplaceRequest,
    RegexReplaceResponse,
)
from services.replacement import RegexReplacementError, replace_matches
from services.regex_generator import RegexGenerationError, generate_regex


router = Router(tags=["regex"])


@router.post(
    "/regex/generate",
    response={
        200: RegexGenerateResponse,
        400: ErrorResponse,
        422: ErrorResponse,
        429: ErrorResponse,
        502: ErrorResponse,
        503: ErrorResponse,
        504: ErrorResponse,
    },
)
def generate_regex_route(request, payload: RegexGenerateRequest):
    try:
        return generate_regex(
            natural_language=payload.natural_language,
            target_column=payload.target_column,
            sample_values=payload.sample_values,
        )
    except RegexGenerationError as exc:
        return exc.status_code, {
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        }


@router.post("/regex/replace", response={200: RegexReplaceResponse, 400: ErrorResponse})
def replace_regex_route(request, payload: RegexReplaceRequest):
    try:
        return replace_matches(
            columns=payload.columns,
            rows=payload.rows,
            target_column=payload.target_column,
            regex=payload.regex,
            replacement=payload.replacement,
        )
    except RegexReplacementError as exc:
        return exc.status_code, {
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        }
