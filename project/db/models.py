from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    ForeignKey,
    Boolean,
    CheckConstraint,
    Numeric,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ElementInfrastruktury(Base):
    __tablename__ = "elementy_infrastruktury"

    id = Column(Integer, primary_key=True)
    typ = Column(Integer, ForeignKey("typy_infrastruktury.id"), nullable=False)
    lokalizacja = Column(Integer, ForeignKey("lokalizacje.id"), nullable=False)
    obiekt = Column(Integer, ForeignKey("obiekty.id"), nullable=False)
    status = Column(Integer, ForeignKey("statusy_elementow.id"), nullable=False)
    opis = Column(String(1024), nullable=False)
    max_interwal = Column(Integer, nullable=False)


class TypInfrastruktury(Base):
    __tablename__ = "typy_infrastruktury"

    id = Column(Integer, primary_key=True)
    typ = Column(String(32), nullable=False)


class Obiekt(Base):
    __tablename__ = "obiekty"

    id = Column(Integer, primary_key=True)
    typ = Column(String(32), nullable=False)
    do_uzytku = Column(Boolean, nullable=False)


class StatusElementu(Base):
    __tablename__ = "statusy_elementow"

    id = Column(Integer, primary_key=True)
    status = Column(String(32), nullable=False)


class Lokalizacja(Base):
    __tablename__ = "lokalizacje"

    id = Column(Integer, primary_key=True)
    szerokosc_geo = Column(Float, nullable=False)
    dlugosc_geo = Column(Float, nullable=False)
    nazwa_miejsca = Column(String(32), nullable=True)


class Monitoring(Base):
    __tablename__ = "monitoring"

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    wartosc_pomiaru = Column(Float, nullable=False)
    czujnik_id = Column(Integer, ForeignKey("czujnik.id"), nullable=False)
    typ_pomiaru_id = Column(Integer, ForeignKey("typ_pomiaru.id"), nullable=False)
    zgloszenie_id = Column(
        Integer, ForeignKey("zgloszenia_przegladow.id"), nullable=True
    )

    # czujnik = relationship("Czujnik", back_populates="monitoring")
    # typ_pomiaru = relationship("TypPomiaru", back_populates="monitoring")
    # zgloszenie = relationship("ZgloszeniePrzegladu", back_populates="monitoring")


class Czujnik(Base):
    __tablename__ = "czujnik"

    id = Column(Integer, primary_key=True)
    lokalizacja_id = Column(Integer, ForeignKey("lokalizacje.id"), nullable=False)

    # monitoring = relationship("Monitoring", back_populates="czujnik")
    # obslugiwane_typy_pomiarow = relationship("ObslugiwaneTypyPomiarow", back_populates="czujnik")


class ObslugiwaneTypyPomiarow(Base):
    __tablename__ = "obslugiwane_typy_pomiarow"

    typ_pomiaru_fk = Column(Integer, ForeignKey("typ_pomiaru.id"), primary_key=True)
    czujnik_fk = Column(Integer, ForeignKey("czujnik.id"), primary_key=True)

    # typ_pomiaru = relationship("TypPomiaru", back_populates="obslugiwane_typy_pomiarow")
    # czujnik = relationship("Czujnik", back_populates="obslugiwane_typy_pomiarow")


class TypPomiaru(Base):
    __tablename__ = "typ_pomiaru"

    id = Column(Integer, primary_key=True)
    typ = Column(String(32), nullable=False)
    jednostka = Column(String(16), nullable=False)

    # monitoring = relationship("Monitoring", back_populates="typ_pomiaru")
    # obslugiwane_typy_pomiarow = relationship("ObslugiwaneTypyPomiarow", back_populates="typ_pomiaru")


class Naprawa(Base):
    __tablename__ = "naprawy"

    id = Column(Integer, primary_key=True)
    powod_id = Column(Integer, ForeignKey("powody_naprawy.id"), nullable=False)
    serwisant_id = Column(Integer, ForeignKey("serwisanci.id"), nullable=False)
    element_id = Column(
        Integer, ForeignKey("elementy_infrastruktury.id"), nullable=False
    )
    data_rozpoczecia = Column(Date, nullable=False)
    data_zakonczenia = Column(Date, nullable=True)
    koszt = Column(Numeric(precision=2), nullable=False)


class PowodNaprawy(Base):
    __tablename__ = "powody_naprawy"
    __table_args__ = (
        CheckConstraint("(przeglad_id IS NULL) <> (zgloszenie_id IS NULL)"),
    )

    id = Column(Integer, primary_key=True)
    przeglad_id = Column(Integer, ForeignKey("przeglady.id"), nullable=True)
    zgloszenie_id = Column(
        Integer, ForeignKey("zgloszenia_naprawy.id"), nullable=True, unique=True
    )
    priorytet = Column(Integer, nullable=False)
    uwagi = Column(String(1024), nullable=True)


class ZgloszenieNaprawy(Base):
    __tablename__ = "zgloszenia_naprawy"

    id = Column(Integer, primary_key=True)
    element_id = Column(
        Integer, ForeignKey("elementy_infrastruktury.id"), nullable=False
    )
    data = Column(Date, nullable=False)
    zglaszajacy = Column(String(64), nullable=False)
    uwagi = Column(String(128), nullable=True)


class Serwisant(Base):
    __tablename__ = "serwisanci"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String(128), nullable=False)
    nr_telefonu = Column(String(32), nullable=False)
    adres_mail = Column(String(128), nullable=False)


class Przeglad(Base):
    __tablename__ = "przeglady"

    id = Column(Integer, primary_key=True)
    typ_przegladu_id = Column(Integer, ForeignKey("typy_przegladow.id"), nullable=False)
    serwisant_id = Column(Integer, ForeignKey("serwisanci.id"), nullable=False)
    powod_id = Column(Integer, ForeignKey("powody_przegladow.id"), nullable=False)
    opis_zakresu_prac = Column(String(1024), nullable=False)
    data_rozpoczecia = Column(Date, nullable=False)
    data_zakonczenia = Column(Date, nullable=True)
    koszt = Column(Numeric(precision=2), nullable=False)


class TypPrzegladu(Base):
    __tablename__ = "typy_przegladow"

    id = Column(Integer, primary_key=True, nullable=False)
    typ = Column(String(128), nullable=False)


class PowodPrzegladu(Base):
    __tablename__ = "powody_przegladow"

    id = Column(Integer, primary_key=True)
    powod = Column(String(128), nullable=False)
    zgloszenie_id = Column(
        Integer, ForeignKey("zgloszenia_przegladow.id"), unique=True, nullable=False
    )


class SprawdzoneElementy(Base):
    __tablename__ = "sprawdzone_elementy"

    przeglad_fk = Column(Integer, ForeignKey("przeglady.id"), primary_key=True)
    element_infrastruktury_fk = Column(
        Integer, ForeignKey("elementy_infrastruktury.id"), primary_key=True
    )


class ZgloszeniePrzegladu(Base):
    __tablename__ = "zgloszenia_przegladow"

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    zglaszajacy = Column(String(32), nullable=False)
    uwagi = Column(String(128), nullable=True)
    element_id = Column(
        Integer, ForeignKey("elementy_infrastruktury.id"), nullable=False
    )


class Uzytkownik(Base):
    __tablename__ = "uzytkownicy"

    id = Column(Integer, primary_key=True)
    rola_fk = Column(Integer, ForeignKey("rola.id"), nullable=False)
    imie = Column(String(32), nullable=False)
    nazwisko = Column(String(32), nullable=True)
    email = Column(String(32), unique=True, nullable=False)
    numer_tel = Column(String(32), nullable=True)


class Rola(Base):
    __tablename__ = "rola"

    id = Column(Integer, primary_key=True)
    rola = Column(String(32), nullable=False)
