from werkzeug.security import generate_password_hash

from project.db.database import db
from project.app import app
from project.db.models import (
    Rola,
    Uzytkownik
)


def create_admin() -> None:
    items = []

    items += [
        Rola(rola="Admin"),

        Uzytkownik(
            rola_fk=1,
            imie="Admin",
            nazwisko="",
            email="admin@example.com",
            numer_tel="123456789",
            password_hash=generate_password_hash("admin"),
        )
    ]

    for item in items:
        db.session.add(item)
    db.session.commit()
    print("Data inserted successfully")


if __name__ == "__main__":
    with app.app_context():
        create_admin()
