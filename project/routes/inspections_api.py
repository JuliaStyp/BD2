import re
from typing import Any, Mapping

from flask import Blueprint, request, jsonify, Response
from sqlalchemy.exc import IntegrityError

from project.db import (
    db,
    Przeglad,
    TypPrzegladu,
    PowodPrzegladu,
    ZgloszeniePrzegladu,
)
from project.db.models import SerializedBase
from project.forms.inspections_forms import (
    TypesForm,
    CausesForm,
    InspectionsForm,
    RequestsForm,
)
from project.utils import admin_required, login_required

inspections_api = Blueprint("inspections_api", __name__, url_prefix="/api/inspections")


@inspections_api.route("/", methods=["GET"])
@login_required
def all_inspections() -> list[dict[str, Any]]:
    return select_by_page(table=Przeglad, orderby=Przeglad.data_rozpoczecia)


@inspections_api.route("/", methods=["POST"])
@login_required
def create_inspection() -> dict[str, Any]:
    form = InspectionsForm(request.form)
    if not form.validate():
        return {"message": form.errors.popitem()[0][1]}
    values = dict(request.form)
    values.pop("serwisant")
    values.pop("powod")
    values.pop("typ_przegladu")

    values["serwisant_id"] = form.serwisant_id
    values["powod_id"] = form.powod_id
    values["typ_przegladu_id"] = form.typ_przegladu_id
    if not values["data_zakonczenia"]:
        values["data_zakonczenia"] = None
    return insert(table=Przeglad, values=values)


@inspections_api.route("/<inspection_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_inspection(inspection_id: int) -> Response:
    return delete_by_id(table=Przeglad, id=inspection_id)


@inspections_api.route("/types", methods=["GET"])
@login_required
def all_types() -> list[dict[str, Any]]:
    return select_by_page(table=TypPrzegladu, orderby=TypPrzegladu.typ)


@inspections_api.route("/types", methods=["POST"])
@login_required
def create_type() -> dict[str, Any]:
    form = TypesForm(request.form)
    if not form.validate():
        return {"message": form.errors["typ"]}
    return insert(table=TypPrzegladu, values=request.form)


@inspections_api.route("/types/<type_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_type(type_id: int) -> Response:
    return delete_by_id(table=TypPrzegladu, id=type_id)


@inspections_api.route("/causes", methods=["GET"])
@login_required
def get_cause() -> list[dict[str, Any]]:
    return select_by_page(table=PowodPrzegladu, orderby=PowodPrzegladu.id)


@inspections_api.route("/causes", methods=["POST"])
@login_required
def create_cause() -> dict[str, Any]:
    form = CausesForm(request.form)
    if not form.validate():
        return {"message": form.errors["zgloszenie"]}
    values = dict(request.form)
    values.pop("zgloszenie")
    values["zgloszenie_id"] = form.zgloszenie_id
    return insert(table=PowodPrzegladu, values=values)


@inspections_api.route("/causes/<cause_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_cause(cause_id: int) -> Response:
    return delete_by_id(table=PowodPrzegladu, id=cause_id)


@inspections_api.route("/requests", methods=["GET"])
@login_required
def all_requests() -> list[dict[str, Any]]:
    return select_by_page(table=ZgloszeniePrzegladu, orderby=ZgloszeniePrzegladu.data)


@inspections_api.route("/requests", methods=["POST"])
@login_required
def create_request() -> dict[str, Any]:
    form = RequestsForm(request.form)
    if not form.validate():
        return {"message": form.errors["data"]}
    return insert(table=ZgloszeniePrzegladu, values=dict(request.form))


@inspections_api.route("/requests/<request_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_request(request_id: int) -> Response:
    return delete_by_id(table=ZgloszeniePrzegladu, id=request_id)


def insert(table: Any, values: Mapping[str, Any]) -> dict[str, Any]:
    item: SerializedBase = table(**values)
    db.session.add(item)
    db.session.commit()
    return {"message": "Obiekt dodany", "item": item.to_dict()}


def select_by_page(table: Any, orderby: Any) -> list[dict[str, Any]]:
    page: int = int(request.args.get("page", 1))
    page_size: int = int(request.args.get("page-size", 15))
    idx = page * page_size
    all_items = db.session.query(table).order_by(orderby)
    return [i.to_dict() for i in all_items[idx - page_size : idx]]


def delete_by_id(table: Any, id: int) -> Response:
    to_delete = db.session.query(table).where(table.id == id).one_or_none()
    if to_delete is None:
        return jsonify({"message": "Obiekt nie istnieje"})
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        return jsonify({"message": errorMessage(err.args[0])})
    return jsonify({"message": "Obiekt pomyślnie usunięty"})


def errorMessage(error):
    table = ERROR_TABLE.findall(error)[0]
    return (
        f"Nie można usunąć obiektu - odwołuje się do niego obiekt z tabeli '{table[1]}'"
    )


ERROR_TABLE = re.compile(
    r'relation "([^"]+)"|from table "([^"]+)|odwołanie w tabeli "([^"]+)'
)
