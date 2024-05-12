import os

import structlog
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy

log = structlog.getLogger()

engine = create_engine(os.environ["DB_URL"])
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

db = SQLAlchemy()

def init() -> None:
    from project.db.models import Base

    Base.query = db_session.query_property()
    Base.metadata.create_all(engine)
    log.info(f"Created {len(Base.metadata.tables)} tables")