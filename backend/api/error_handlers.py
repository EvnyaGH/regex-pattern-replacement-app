from ninja import NinjaAPI
from ninja.errors import HttpError, ValidationError


def register_error_handlers(api: NinjaAPI) -> None:
    @api.exception_handler(ValidationError)
    def handle_validation_error(request, exc):
        return api.create_response(
            request,
            {
                "error": {
                    "code": "REQUEST_VALIDATION_ERROR",
                    "message": "One or more request fields are missing or invalid.",
                    "details": {"fields": exc.errors},
                }
            },
            status=422,
        )

    @api.exception_handler(HttpError)
    def handle_http_error(request, exc):
        code = "INVALID_REQUEST_BODY" if exc.status_code == 400 else "HTTP_ERROR"
        return api.create_response(
            request,
            {
                "error": {
                    "code": code,
                    "message": str(exc),
                    "details": {},
                }
            },
            status=exc.status_code,
        )
