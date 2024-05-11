from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Naprawa(Base):
    __tablename__ = "naprawy"

    id = Column(Integer, primary_key=True)
    powod_id = Column(Integer, ForeignKey("powody.id"))
    serwisant_id = Column(Integer, ForeignKey("serwisanci.id"))
    element_id = Column(Integer, ForeignKey("elementy.id"))


class PowodNaprawy(Base):
    __tablename__ = "powody"

    id = Column(Integer, primary_key=True)
    przeglad_id = Column(Integer, ForeignKey("przeglady.id"))
    zgloszenie_id = Column(Integer, ForeignKey("zgloszenia.id"))
    priorytet = Column(Integer)
    uwagi = Column(String)


class ZgloszenieNaprawy(Base):
    __tablename__ = "zgloszenia"

    id = Column(Integer, primary_key=True)
    element_id = Column(Integer, ForeignKey("elementy.id"))
    data = Column(Date)
    zglaszajacy = Column(String)
    uwagi = Column(String)
