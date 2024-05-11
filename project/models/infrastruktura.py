from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Float
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
    max_interwal = Column(Integer, nullable= False)


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








