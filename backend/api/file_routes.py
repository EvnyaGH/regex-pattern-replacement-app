from ninja import File, Form, Router, UploadedFile

from schemas.error_schemas import ErrorResponse
from schemas.file_schemas import FilePreviewResponse, FileProcessResponse
from services.file_parser import FilePreviewError, build_file_preview
from services.file_processor import process_uploaded_file
from services.replacement import RegexReplacementError


router = Router(tags=["files"])


@router.post("/files/preview", response={200: FilePreviewResponse, 400: ErrorResponse, 413: ErrorResponse})
def preview_file(request, file: UploadedFile = File(...), preview_limit: int = Form(50)):
    try:
        return build_file_preview(file, preview_limit=preview_limit)
    except FilePreviewError as exc:
        return exc.status_code, {
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        }


@router.post("/files/process", response={200: FileProcessResponse, 400: ErrorResponse, 413: ErrorResponse})
def process_file(
    request,
    file: UploadedFile = File(...),
    target_column: str = Form(...),
    regex: str = Form(...),
    replacement: str = Form(""),
    preview_limit: int = Form(50),
):
    try:
        return process_uploaded_file(
            uploaded_file=file,
            target_column=target_column,
            regex=regex,
            replacement=replacement,
            preview_limit=preview_limit,
        )
    except (FilePreviewError, RegexReplacementError) as exc:
        return exc.status_code, {
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        }
