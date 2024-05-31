import re
from typing import Any

from wtforms import (
    Form,
    TextAreaField,
    DateField,
    DecimalField,
    SelectField,
)
from wtforms.validators import (
    NumberRange,
    Length,
    Optional,
    DataRequired,
    StopValidation,
)

from project.db import (
    db,
    TypPrzegladu,
    PowodPrzegladu,
    Serwisant,
    ZgloszeniePrzegladu,
    ElementInfrastruktury,
)


def unique(table: Any, column: Any, value: Any):
    if not (db.session.query(table).where(column == value).one_or_none() is None):
        raise StopValidation(f"Obiekt o wartości {column.name}={value} już istnieje")


def inspectionTypes():
    ret = db.session.query(TypPrzegladu.typ).order_by(TypPrzegladu.typ).all()
    return [i[0] for i in ret]


def services():
    ret = db.session.query(Serwisant.id, Serwisant.nazwa).order_by(Serwisant.id).all()
    return [f"{i[0]}. {i[1]}" for i in ret]


def causes():
    ret = (
        db.session.query(
            PowodPrzegladu.id, PowodPrzegladu.zgloszenie_id, PowodPrzegladu.powod
        )
        .order_by(PowodPrzegladu.id)
        .all()
    )
    return [f"Powód: {i[0]} (Zgłoszenie: {i[1]}, {i[2]})" for i in ret]


def requestValues():
    ret = (
        db.session.query(
            ZgloszeniePrzegladu.id,
            ZgloszeniePrzegladu.data,
            ZgloszeniePrzegladu.element_id,
        )
        .order_by(ZgloszeniePrzegladu.id)
        .all()
    )
    return [f"Zgloszenie: {i[0]} ({i[1]}, element: {i[2]})" for i in ret]


def elements():
    ret = (
        db.session.query(
            ElementInfrastruktury.id,
        )
        .order_by(ElementInfrastruktury.id)
        .all()
    )
    return [i[0] for i in ret]


class InspectionsForm(Form):
    typ_przegladu = SelectField(
        "Typ", choices=inspectionTypes, validators=[DataRequired()]
    )
    serwisant = SelectField("Serwisant", choices=services, validators=[DataRequired()])
    powod = SelectField("Powód", choices=causes, validators=[DataRequired()])
    opis_zakresu_prac = TextAreaField(
        "Opis zakresu prac",
        validators=[
            Length(min=0, max=1024, message="Maksymalnie 1024 znaków"),
            DataRequired(),
        ],
    )
    data_rozpoczecia = DateField("Data rozpoczęcia", validators=[DataRequired()])
    data_zakonczenia = DateField("Data zakończenia", validators=[Optional()])
    koszt = DecimalField(
        "Koszt",
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=0, message="Wartość nie może być ujemna"),
        ],
    )

    @property
    def typ_przegladu_id(self):
        value = self.typ_przegladu.data
        return db.session.query(TypPrzegladu).where(TypPrzegladu.typ == value).one().id

    @property
    def serwisant_id(self):
        return self.serwisant.data.split(".")[0]

    @property
    def powod_id(self):
        item_id = re.compile(r"^[^:]+: (\d+) .+$")
        return item_id.findall(self.powod.data)[0]


class TypesForm(Form):
    typ = TextAreaField(
        "Typ",
        validators=[
            Length(min=0, max=128, message="Maksymalnie 128 znaków"),
            DataRequired(),
        ],
    )

    def validate_typ(self, field):
        unique(TypPrzegladu, TypPrzegladu.typ, field.data)


class CausesForm(Form):
    powod = TextAreaField(
        "Powód zgłoszenia",
        validators=[
            Length(min=0, max=128, message="Maksymalnie 128 znaków"),
            DataRequired(),
        ],
    )
    zgloszenie = SelectField(
        "ID zgłoszenia", choices=requestValues, validators=[DataRequired()]
    )

    def validate_zgloszenie(self, field):
        unique(PowodPrzegladu, PowodPrzegladu.zgloszenie_id, self.zgloszenie_id)

    @property
    def zgloszenie_id(self):
        item_id = re.compile(r"^[^:]+: (\d+) .+$")
        return item_id.findall(self.zgloszenie.data)[0]


class RequestsForm(Form):
    data = DateField("Data", validators=[DataRequired()])
    zglaszajacy = TextAreaField(
        "Zgłaszający",
        validators=[
            Length(min=0, max=32, message="Maksymalnie 32 znaków"),
            DataRequired(),
        ],
    )
    uwagi = TextAreaField(
        "Uwagi",
        validators=[
            Length(min=0, max=128, message="Maksymalnie 128 znaków"),
            Optional(),
        ],
    )
    element_id = SelectField(
        "Element infrastruktury", choices=elements, validators=[DataRequired()]
    )
