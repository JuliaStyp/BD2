from sqlalchemy import create_engine
from models import Base

if __name__ == "__main__":
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    Base.metadata.bind = engine
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
