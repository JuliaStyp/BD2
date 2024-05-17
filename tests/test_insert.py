from werkzeug.security import generate_password_hash

from project.db.database import db
from project.app import app
from project.db.models import (
    Rola,
    Uzytkownik,
    Serwisant,
    TypInfrastruktury,
    Obiekt,
    StatusElementu,
    Lokalizacja,
    ElementInfrastruktury,
    TypPrzegladu,
    ZgloszeniePrzegladu,
    PowodPrzegladu,
    Przeglad,
    ZgloszenieNaprawy,
    PowodNaprawy,
    Naprawa,
)


def insert_data() -> None:
    items = []

    items += [
        TypInfrastruktury(typ="Typ Infrastruktury Pierwszy"),
        TypInfrastruktury(typ="Typ Infrastruktury Drugi"),
        TypInfrastruktury(typ="Typ Infrastruktury Trzeci"),
        TypInfrastruktury(typ="Typ Infrastruktury Czwarty"),
    ]

    items += [
        Obiekt(typ="Obiekt Pierwszy", do_uzytku=True),
        Obiekt(typ="Obiekt Drugi", do_uzytku=True),
        Obiekt(typ="Obiekt Trzeci", do_uzytku=True),
        Obiekt(typ="Obiekt Czwarty", do_uzytku=True),
        Obiekt(typ="Obiekt Piąty", do_uzytku=True),
        Obiekt(typ="Obiekt Szósty", do_uzytku=False),
        Obiekt(typ="Obiekt Siódmy", do_uzytku=False),
        Obiekt(typ="Obiekt Ósmy", do_uzytku=False),
        Obiekt(typ="Obiekt Dziewiąty", do_uzytku=False),
        Obiekt(typ="Obiekt Dziesiąty", do_uzytku=False),
    ]

    items += [
        StatusElementu(status="Status Pierwszy"),
        StatusElementu(status="Status Drugi"),
        StatusElementu(status="Status Trzeci"),
        StatusElementu(status="Status Czwarty"),
    ]

    items += [
        Lokalizacja(
            szerokosc_geo=52.00, dlugosc_geo=21.400, nazwa_miejsca="Miejsce Pierwsze"
        ),
        Lokalizacja(
            szerokosc_geo=55.251, dlugosc_geo=18.403, nazwa_miejsca="Miejsce Drugie"
        ),
        Lokalizacja(
            szerokosc_geo=51.222, dlugosc_geo=15.400, nazwa_miejsca="Miejsce Trzecie"
        ),
        Lokalizacja(
            szerokosc_geo=50.21001, dlugosc_geo=15.2322, nazwa_miejsca="Miejsce Czwarte"
        ),
        Lokalizacja(
            szerokosc_geo=50.100, dlugosc_geo=5.2503, nazwa_miejsca="Miejsce Piąte"
        ),
        Lokalizacja(
            szerokosc_geo=56.67003,
            dlugosc_geo=-3.244001,
            nazwa_miejsca="Miejsce Szóste",
        ),
        Lokalizacja(
            szerokosc_geo=69.21370, dlugosc_geo=27.24202, nazwa_miejsca="Miejsce Siódme"
        ),
        Lokalizacja(
            szerokosc_geo=60.23001, dlugosc_geo=18.3232, nazwa_miejsca="Miejsce Ósme"
        ),
    ]

    items += [
        ElementInfrastruktury(
            typ=1, lokalizacja=1, opis="element1", max_interwal=365, obiekt=1, status=1
        ),
        ElementInfrastruktury(
            typ=2, lokalizacja=1, opis="element2", max_interwal=365, obiekt=1, status=1
        ),
        ElementInfrastruktury(
            typ=3, lokalizacja=1, opis="element3", max_interwal=365, obiekt=1, status=4
        ),
        ElementInfrastruktury(
            typ=4, lokalizacja=2, opis="element4", max_interwal=365, obiekt=2, status=1
        ),
        ElementInfrastruktury(
            typ=4, lokalizacja=2, opis="element5", max_interwal=365, obiekt=2, status=1
        ),
        ElementInfrastruktury(
            typ=3, lokalizacja=2, opis="element6", max_interwal=180, obiekt=3, status=1
        ),
        ElementInfrastruktury(
            typ=2, lokalizacja=4, opis="element7", max_interwal=365, obiekt=4, status=3
        ),
        ElementInfrastruktury(
            typ=2, lokalizacja=4, opis="element8", max_interwal=365, obiekt=4, status=2
        ),
        ElementInfrastruktury(
            typ=3, lokalizacja=4, opis="element9", max_interwal=365, obiekt=4, status=2
        ),
        ElementInfrastruktury(
            typ=2, lokalizacja=5, opis="element10", max_interwal=365, obiekt=4, status=4
        ),
        ElementInfrastruktury(
            typ=4, lokalizacja=5, opis="element11", max_interwal=365, obiekt=5, status=3
        ),
        ElementInfrastruktury(
            typ=3, lokalizacja=5, opis="element12", max_interwal=365, obiekt=5, status=3
        ),
        ElementInfrastruktury(
            typ=1, lokalizacja=6, opis="element13", max_interwal=365, obiekt=6, status=1
        ),
        ElementInfrastruktury(
            typ=1, lokalizacja=6, opis="element14", max_interwal=365, obiekt=6, status=1
        ),
        ElementInfrastruktury(
            typ=1, lokalizacja=6, opis="element15", max_interwal=365, obiekt=7, status=3
        ),
        ElementInfrastruktury(
            typ=2, lokalizacja=7, opis="element16", max_interwal=365, obiekt=8, status=2
        ),
        ElementInfrastruktury(
            typ=2, lokalizacja=7, opis="element17", max_interwal=365, obiekt=8, status=2
        ),
        ElementInfrastruktury(
            typ=3, lokalizacja=8, opis="element18", max_interwal=800, obiekt=9, status=1
        ),
        ElementInfrastruktury(
            typ=3, lokalizacja=8, opis="element19", max_interwal=800, obiekt=9, status=1
        ),
        ElementInfrastruktury(
            typ=4,
            lokalizacja=8,
            opis="element20",
            max_interwal=365,
            obiekt=10,
            status=1,
        ),
        ElementInfrastruktury(
            typ=3,
            lokalizacja=8,
            opis="element21",
            max_interwal=365,
            obiekt=10,
            status=1,
        ),
    ]

    # Example service
    items += [
        Serwisant(
            nazwa="Serwisant Pierwszy",
            nr_telefonu="123456789",
            adres_mail="serwisant1@mail.pl",
        ),
        Serwisant(
            nazwa="Serwisant Drugi",
            nr_telefonu="987654321",
            adres_mail="serwisant2@mail.pl",
        ),
        Serwisant(
            nazwa="Serwisant Trzeci",
            nr_telefonu="098765432",
            adres_mail="serwisant3@mail.pl",
        ),
        Serwisant(
            nazwa="Serwisant Czwarty",
            nr_telefonu="111222333",
            adres_mail="serwisant4@mail.pl",
        ),
    ]

    # Example roles
    items += [Rola(rola="Admin"), Rola(rola="Użytkownik")]

    # Example users
    items += [
        Uzytkownik(
            rola_fk=1,
            imie="Marcin",
            nazwisko="S",
            email="marcin@example.com",
            numer_tel="123456789",
            password_hash=generate_password_hash("haslo"),
        ),
        Uzytkownik(
            rola_fk=1,
            imie="Maciej",
            nazwisko="D",
            email="maciej@example.com",
            numer_tel="987654321",
            password_hash=generate_password_hash("haslo"),
        ),
        Uzytkownik(
            rola_fk=1,
            imie="Tomasz",
            nazwisko="K",
            email="tomasz@example.com",
            numer_tel="501997443",
            password_hash=generate_password_hash("haslo"),
        ),
        Uzytkownik(
            rola_fk=1,
            imie="Julia",
            nazwisko="S",
            email="julia@example.com",
            numer_tel="946547832",
            password_hash=generate_password_hash("haslo"),
        ),
        Uzytkownik(
            rola_fk=1,
            imie="Michał",
            nazwisko="G",
            email="michal@example.com",
            numer_tel="329047251",
            password_hash=generate_password_hash("haslo"),
        ),
        Uzytkownik(
            rola_fk=2,
            imie="Jan",
            nazwisko="Kowalski",
            email="jan.k@example.com",
            numer_tel="505764384",
            password_hash=generate_password_hash("haslo"),
        ),
    ]

    for i in range(1, 5):
        items.append(TypPrzegladu(typ=i))

    items += [
        ZgloszeniePrzegladu(
            data="2024-04-01",
            zglaszajacy="Pracownik1",
            uwagi="Bardzo nie działa",
            element_id=1,
        ),
        ZgloszeniePrzegladu(data="2024-04-02", zglaszajacy="Pracownik1", element_id=1),
        ZgloszeniePrzegladu(data="2024-04-03", zglaszajacy="Pracownik1", element_id=2),
        ZgloszeniePrzegladu(
            data="2024-04-04",
            zglaszajacy="Pracownik2",
            uwagi="Nic nie działa",
            element_id=3,
        ),
        ZgloszeniePrzegladu(data="2024-04-05", zglaszajacy="Pracownik2", element_id=4),
    ]

    items += [
        PowodPrzegladu(powod="Awaria", zgloszenie_id=1),
        PowodPrzegladu(powod="Awaria", zgloszenie_id=2),
        PowodPrzegladu(powod="Przegląd okresowy", zgloszenie_id=3),
        PowodPrzegladu(powod="Awaria", zgloszenie_id=4),
        PowodPrzegladu(powod="Przegląd okresowy", zgloszenie_id=5),
    ]

    items += [
        Przeglad(
            typ_przegladu_id=1,
            serwisant_id=1,
            powod_id=1,
            opis_zakresu_prac="Bardzo duzy zakres prac",
            data_rozpoczecia="2024-04-10",
            koszt=100000.50,
        ),
        Przeglad(
            typ_przegladu_id=2,
            serwisant_id=2,
            powod_id=2,
            opis_zakresu_prac="Mały zakres prac",
            data_rozpoczecia="2024-04-11",
            koszt=19999.99,
        ),
        Przeglad(
            typ_przegladu_id=3,
            serwisant_id=3,
            powod_id=3,
            opis_zakresu_prac="Drobne usterki",
            data_rozpoczecia="2024-04-12",
            koszt=123456789.10,
        ),
        Przeglad(
            typ_przegladu_id=4,
            serwisant_id=4,
            powod_id=4,
            opis_zakresu_prac="Nic nie dziala, wszystko do wymiany",
            data_rozpoczecia="2024-04-13",
            koszt=3999.99,
        ),
        Przeglad(
            typ_przegladu_id=4,
            serwisant_id=4,
            powod_id=5,
            opis_zakresu_prac="Drobne usterki",
            data_rozpoczecia="2024-04-14",
            koszt=1212.12,
        ),
    ]

    items += [
        ZgloszenieNaprawy(
            element_id=1,
            data='2024-04-13',
            zglaszajacy="Mechanik1",
            uwagi="Uszczelka pod głowicą chyba"
        ),

        ZgloszenieNaprawy(
            element_id=2,
            data='2024-03-13',
            zglaszajacy="Mechanik1",
            uwagi="Pękła rura"
        ),

        ZgloszenieNaprawy(
            element_id=3,
            data='2024-04-18',
            zglaszajacy="Mechanik2",
            uwagi="Łożysko wydaje dziwne dźwięki"
        ),

        ZgloszenieNaprawy(
            element_id=4,
            data='2024-05-12',
            zglaszajacy="Mechanik3",
            uwagi="Chwieje się podczas pracy"
        ),

        ZgloszenieNaprawy(
            element_id=5,
            data='2024-05-10',
            zglaszajacy="Mechanik4",
            uwagi="Przecieka"
        ),
    ]

    items += [
        PowodNaprawy(
            przeglad_id=1,
            priorytet=5,
            uwagi="Zagraża integralności systemu przy dalszej eksploatacji"
        ),

        PowodNaprawy(
            przeglad_id=2,
            priorytet=1,
            uwagi="Zagraża integralności systemu przy dalszej eksploatacji"
        ),

        PowodNaprawy(
            przeglad_id=4,
            priorytet=2,
            uwagi="Zagraża integralności systemu przy dalszej eksploatacji"
        ),

        PowodNaprawy(
            zgloszenie_id=1,
            priorytet=4,
            uwagi="Zagraża integralności systemu przy dalszej eksploatacji"
        ),

        PowodNaprawy(
            zgloszenie_id=2,
            priorytet=3,
            uwagi="Zagraża integralności systemu przy dalszej eksploatacji"
        ),
    ]

    items += [
        Naprawa(
            powod_id=4,
            serwisant_id=1,
            element_id=1,
            data_rozpoczecia='2024-05-10',
            data_zakonczenia=None,
            koszt=7312,
        ),

        Naprawa(
            powod_id=5,
            serwisant_id=2,
            element_id=2,
            data_rozpoczecia='2024-04-10',
            data_zakonczenia='2024-05-11',
            koszt=3345,
        ),

        Naprawa(
            powod_id=3,
            serwisant_id=2,
            element_id=3,
            data_rozpoczecia='2024-03-12',
            data_zakonczenia='2024-04-10',
            koszt=43891,
        ),
    ]

    for item in items:
        db.session.add(item)
        db.session.commit()
    print("Data inserted successfully")


if __name__ == "__main__":
    with app.app_context():
        insert_data()

