from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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

    id = Column(Integer, primary_key=True)
    przeglad_id = Column(Integer, ForeignKey("przeglady.id"))
    zgloszenie_id = Column(Integer, ForeignKey("zgloszenia_naprawy.id"))
    priorytet = Column(Integer)
    uwagi = Column(String(1024))


class ZgloszenieNaprawy(Base):
    __tablename__ = "zgloszenia_naprawy"

    id = Column(Integer, primary_key=True)
    element_id = Column(Integer, ForeignKey("elementy.id"))
    data = Column(Date)
    zglaszajacy = Column(String(64))
    uwagi = Column(String(128))
