from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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
    powod_id = Column(Integer, ForeignKey("powody.id"), nullable=False)
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
    zgloszenie_id = Column(Integer, ForeignKey("zgloszenia_przegladow.id"), unique=True, nullable=False)


class SprawdzoneElementy(Base):
    __tablename__ = "sprawdzone_elementy"

    przeglad_fk = Column(Integer, ForeignKey("przeglady.id"), primary_key=True)
    element_infrastruktury_fk = Column(Integer, ForeignKey("elementy_infrastruktury.id"), primary_key=True)


class ZgloszeniePrzegladu(Base):
    __tablename__ = "zgloszenia_przegladow"

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    zglaszajacy = Column(String(32), nullable=False)
    uwagi = Column(String(128), nullable=True)
    element_id = Column(Integer, ForeignKey("elementy_infrastruktury.id"), nullable=False)

