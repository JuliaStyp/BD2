from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
# from przeglady import ZgloszeniePrzegladu

Base = declarative_base()


class Monitoring(Base):
    __tablename__ = "monitoring"

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    wartosc_pomiaru = Column(Float, nullable=False)
    czujnik_id = Column(Integer, ForeignKey("czujnik.id"), nullable=False)
    typ_pomiaru_id = Column(Integer, ForeignKey("typ_pomiaru.id"), nullable=False)
    zgloszenie_id = Column(Integer, ForeignKey("zgloszenie_przegladu.id"), nullable=True)

    czujnik = relationship("Czujnik", back_populates="monitoring")
    typ_pomiaru = relationship("TypPomiaru", back_populates="monitoring")
    zgloszenie = relationship("ZgloszeniePrzegladu", back_populates="monitoring")


class Czujnik(Base):
    __tablename__ = "czujnik"

    id = Column(Integer, primary_key=True)
    lokalizacja_id = Column(Integer, ForeignKey("lokalizacja.id"), nullable=False)

    monitoring = relationship("Monitoring", back_populates="czujnik")
    obslugiwane_typy_pomiarow = relationship("ObslugiwaneTypyPomiarow", back_populates="czujnik")


class ObslugiwaneTypyPomiarow(Base):
    __tablename__ = "obslugiwane_typy_pomiarow"

    typ_pomiaru_fk = Column(Integer, ForeignKey("typ_pomiaru.id"), primary_key=True)
    czujnik_fk = Column(Integer, ForeignKey("czujnik.id"), primary_key=True)

    typ_pomiaru = relationship("TypPomiaru", back_populates="obslugiwane_typy_pomiarow")
    czujnik = relationship("Czujnik", back_populates="obslugiwane_typy_pomiarow")


class TypPomiaru(Base):
    __tablename__ = "typ_pomiaru"

    id = Column(Integer, primary_key=True)
    typ = Column(String(32), nullable=False)
    jednostka = Column(String(16), nullable=False)

    monitoring = relationship("Monitoring", back_populates="typ_pomiaru")
    obslugiwane_typy_pomiarow = relationship("ObslugiwaneTypyPomiarow", back_populates="typ_pomiaru")
