from ninja import NinjaAPI

from api.error_handlers import register_error_handlers
from api.file_routes import router as file_router
from api.health_routes import router as health_router
from api.regex_routes import router as regex_router


api = NinjaAPI(
    title="Regex Pattern Replacement API",
    version="0.1.0",
)

register_error_handlers(api)
api.add_router("", health_router)
api.add_router("", file_router)
api.add_router("", regex_router)
