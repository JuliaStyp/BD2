from .auth import auth_bp
from .inspections import inspections_api
from .index import index_bp
from .repairs import repairs_bp
from .service import service_bp
from .infrastructure import infr_bp
from .inspections_ui import inspections_ui
from .reports import reports_bp

__all__ = [
    "auth_bp",
    "index_bp",
    "repairs_bp",
    "service_bp",
    "infr_bp",
    "inspections_ui",
    "inspections_api",
    "reports_bp",
]
