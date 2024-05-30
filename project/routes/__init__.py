from .auth import auth_bp
from .inspections import inspections_bp
from .index import index_bp
from .repairs import repairs_bp
from .service import service_bp
from .infrastructure import infr_bp

__all__ = ["auth_bp", "inspections_bp", "index_bp", "repairs_bp", "service_bp", "infr_bp"]
