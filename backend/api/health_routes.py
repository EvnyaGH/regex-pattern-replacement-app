from ninja import Router

from schemas.health_schemas import HealthResponse


router = Router(tags=["health"])


@router.get("/health", response=HealthResponse)
def health(request):
    return {"status": "ok"}
