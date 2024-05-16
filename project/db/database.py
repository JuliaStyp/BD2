import os

import structlog
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


log = structlog.getLogger()

engine = create_engine(os.environ["DB_URL"])
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

db = SQLAlchemy()


def init_db() -> None:
    from .models import Base

    Base.query = db_session.query_property()
    Base.metadata.create_all(engine)
    log.info(f"Created {len(Base.metadata.tables)} tables")


def clear_db() -> None:
    db.reflect()

    db.drop_all()

    print("All tables dropped successfully.")


def insert_data() -> None:
    from .models import Rola, Uzytkownik
    from werkzeug.security import generate_password_hash

    # Example roles
    roles = [
        Rola(rola="Admin"),
        Rola(rola="Użytkownik")
    ]

    # Example users
    users = [
        Uzytkownik(
            rola_fk=1,
            imie="Marcin",
            nazwisko="S",
            email="marcin@example.com",
            numer_tel="123456789",
            password_hash=generate_password_hash("haslo")
        ),
        Uzytkownik(
            rola_fk=1,
            imie="Maciej",
            nazwisko="D",
            email="maciej@example.com",
            numer_tel="987654321",
            password_hash=generate_password_hash("haslo")
        ),
        Uzytkownik(
            rola_fk=1,
            imie="Tomasz",
            nazwisko="K",
            email="tomasz@example.com",
            numer_tel="501997443",
            password_hash=generate_password_hash("haslo")
        ),
        Uzytkownik(
            rola_fk=1,
            imie="Julia",
            nazwisko="S",
            email="julia@example.com",
            numer_tel="946547832",
            password_hash=generate_password_hash("haslo")
        ),
        Uzytkownik(
            rola_fk=1,
            imie="Michał",
            nazwisko="G",
            email="michal@example.com",
            numer_tel="329047251",
            password_hash=generate_password_hash("haslo")
        ),
        Uzytkownik(
            rola_fk=2,
            imie="Jan",
            nazwisko="Kowalski",
            email="jan.k@example.com",
            numer_tel="505764384",
            password_hash=generate_password_hash("haslo")
        )
    ]

    for role in roles:
        db.session.add(role)
    db.session.commit()

    for user in users:
        db.session.add(user)
    db.session.commit()

    print("Data inserted successfully")

