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
    from .models import (
        Rola, Uzytkownik, Serwisant, TypInfrastruktury, Obiekt, StatusElementu,
        Lokalizacja, ElementInfrastruktury
    )
    from werkzeug.security import generate_password_hash
    
    infrastructure_types = [
        TypInfrastruktury(
            typ="Typ Infrastruktury Pierwszy"
        ),
        TypInfrastruktury(
            typ="Typ Infrastruktury Drugi"
        ),
        TypInfrastruktury(
            typ="Typ Infrastruktury Trzeci"
        ),
        TypInfrastruktury(
            typ="Typ Infrastruktury Czwarty"
        )
    ]

    objects = [
        Obiekt (
            typ="Obiekt Pierwszy",
            do_uzytku=True
        ),
        Obiekt (
            typ="Obiekt Drugi",
            do_uzytku=True
        ),
        Obiekt (
            typ="Obiekt Trzeci",
            do_uzytku=True
        ),
        Obiekt (
            typ="Obiekt Czwarty",
            do_uzytku=True
        ),
        Obiekt (
            typ="Obiekt Piąty",
            do_uzytku=True
        ),
        Obiekt (
            typ="Obiekt Szósty",
            do_uzytku=False
        ),
        Obiekt (
            typ="Obiekt Siódmy",
            do_uzytku=False
        ),
        Obiekt (
            typ="Obiekt Ósmy",
            do_uzytku=False
        ),
        Obiekt (
            typ="Obiekt Dziewiąty",
            do_uzytku=False
        ),
        Obiekt (
            typ="Obiekt Dziesiąty",
            do_uzytku=False
        )
    ]

    element_statuses = [
        StatusElementu(
            status="Status Pierwszy"
        ),
        StatusElementu(
            status="Status Drugi"
        ),
        StatusElementu(
            status="Status Trzeci"
        ),
        StatusElementu(
            status="Status Czwarty"
        ),
    ]

    localizations = [
        Lokalizacja(
            szerokosc_geo=52.00,
            dlugosc_geo=21.400,
            nazwa_miejsca='Miejsce Pierwsze'
        ),
        Lokalizacja(
            szerokosc_geo=55.251,
            dlugosc_geo=18.403,
            nazwa_miejsca='Miejsce Drugie'
        ),
        Lokalizacja(
            szerokosc_geo=51.222,
            dlugosc_geo=15.400,
            nazwa_miejsca='Miejsce Trzecie'
        ),
        Lokalizacja(
            szerokosc_geo=50.21001,
            dlugosc_geo=15.2322,
            nazwa_miejsca='Miejsce Czwarte'
        ),
        Lokalizacja(
            szerokosc_geo=50.100,
            dlugosc_geo=5.2503,
            nazwa_miejsca='Miejsce Piąte'
        ),
        Lokalizacja(
            szerokosc_geo=56.67003,
            dlugosc_geo=-3.244001,
            nazwa_miejsca='Miejsce Szóste'
        ),
        Lokalizacja(
            szerokosc_geo=69.21370,
            dlugosc_geo=27.24202,
            nazwa_miejsca='Miejsce Siódme'
        ),
        Lokalizacja(
            szerokosc_geo=60.23001,
            dlugosc_geo=18.3232,
            nazwa_miejsca='Miejsce Ósme'
        )
    ]

    infrastructure_elements = [
        ElementInfrastruktury (
            typ=1,
            lokalizacja=1,
            opis='element1',
            max_interwal=365,
            obiekt=1,
            status=1
        ),
        ElementInfrastruktury (
            typ=2,
            lokalizacja=1,
            opis='element2',
            max_interwal=365,
            obiekt=1,
            status=1
        ),
        ElementInfrastruktury (
            typ=3,
            lokalizacja=1,
            opis='element3',
            max_interwal=365,
            obiekt=1,
            status=4
        ),
        ElementInfrastruktury (
            typ=4,
            lokalizacja=2,
            opis='element4',
            max_interwal=365,
            obiekt=2,
            status=1
        ),
        ElementInfrastruktury (
            typ=4,
            lokalizacja=2,
            opis='element5',
            max_interwal=365,
            obiekt=2,
            status=1
        ),
        ElementInfrastruktury (
            typ=3,
            lokalizacja=2,
            opis='element6',
            max_interwal=180,
            obiekt=3,
            status=1
        ),
        ElementInfrastruktury (
            typ=2,
            lokalizacja=4,
            opis='element7',
            max_interwal=365,
            obiekt=4,
            status=3
        ),
        ElementInfrastruktury (
            typ=2,
            lokalizacja=4,
            opis='element8',
            max_interwal=365,
            obiekt=4,
            status=2
        ),
        ElementInfrastruktury (
            typ=3,
            lokalizacja=4,
            opis='element9',
            max_interwal=365,
            obiekt=4,
            status=2
        ),
        ElementInfrastruktury (
            typ=2,
            lokalizacja=5,
            opis='element10',
            max_interwal=365,
            obiekt=4,
            status=4
        ),
        ElementInfrastruktury (
            typ=4,
            lokalizacja=5,
            opis='element11',
            max_interwal=365,
            obiekt=5,
            status=3
        ),
        ElementInfrastruktury (
            typ=3,
            lokalizacja=5,
            opis='element12',
            max_interwal=365,
            obiekt=5,
            status=3
        ),
        ElementInfrastruktury (
            typ=1,
            lokalizacja=6,
            opis='element13',
            max_interwal=365,
            obiekt=6,
            status=1
        ),
        ElementInfrastruktury (
            typ=1,
            lokalizacja=6,
            opis='element14',
            max_interwal=365,
            obiekt=6,
            status=1
        ),
        ElementInfrastruktury (
            typ=1,
            lokalizacja=6,
            opis='element15',
            max_interwal=365,
            obiekt=7,
            status=3
        ),
        ElementInfrastruktury (
            typ=2,
            lokalizacja=7,
            opis='element16',
            max_interwal=365,
            obiekt=8,
            status=2
        ),
        ElementInfrastruktury (
            typ=2,
            lokalizacja=7,
            opis='element17',
            max_interwal=365,
            obiekt=8,
            status=2
        ),
        ElementInfrastruktury (
            typ=3,
            lokalizacja=8,
            opis='element18',
            max_interwal=800,
            obiekt=9,
            status=1
        ),
        ElementInfrastruktury (
            typ=3,
            lokalizacja=8,
            opis='element19',
            max_interwal=800,
            obiekt=9,
            status=1
        ),
        ElementInfrastruktury (
            typ=4,
            lokalizacja=8,
            opis='element20',
            max_interwal=365,
            obiekt=10,
            status=1
        ),
        ElementInfrastruktury (
            typ=3,
            lokalizacja=8,
            opis='element21',
            max_interwal=365,
            obiekt=10,
            status=1
        ),
    ]

    # Example service
    services = [
        Serwisant(
            nazwa="Serwisant Pierwszy",
            nr_telefonu="123456789",
            adres_mail="serwisant1@mail.pl"
        ),
        Serwisant(
            nazwa="Serwisant Drugi",
            nr_telefonu="987654321",
            adres_mail="serwisant2@mail.pl"
        ),
        Serwisant(
            nazwa="Serwisant Trzeci",
            nr_telefonu="098765432",
            adres_mail="serwisant3@mail.pl"
        ),
        Serwisant(
            nazwa="Serwisant Czwarty",
            nr_telefonu="111222333",
            adres_mail="serwisant4@mail.pl"
        )
    ]

        

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

    for status in element_statuses:
        db.session.add(status)
    db.session.commit()

    for localization in localizations:
        db.session.add(localization)
    db.session.commit()

    for object in objects:
        db.session.add(object)
    db.session.commit()

    for infrastructure_type in infrastructure_types:
        db.session.add(infrastructure_type)
    db.session.commit()

    for infrastructure_el in infrastructure_elements:
        db.session.add(infrastructure_el)
    db.session.commit()

    for service in services:
        db.session.add(service)
    db.session.commit()

    for role in roles:
        db.session.add(role)
    db.session.commit()

    for user in users:
        db.session.add(user)
    db.session.commit()

    print("Data inserted successfully")

