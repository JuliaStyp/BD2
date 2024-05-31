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

inspections_api = Blueprint(
    "inspections_api", __name__, url_prefix="/api/inspections"
)


@inspections_api.route("/", methods=["GET"])
def all_inspections() -> list[dict[str, Any]]:
    return select_by_page(table=Przeglad, orderby=Przeglad.data_rozpoczecia)


@inspections_api.route("/", methods=["POST"])
def create_inspection() -> dict[str, Any]:
    return insert(table=Przeglad, values=request.form)


@inspections_api.route("/<inspection_id>", methods=["DELETE"])
def delete_inspection(inspection_id: int) -> Response:
    return delete_by_id(table=Przeglad, id=inspection_id)


@inspections_api.route("/types", methods=["GET"])
def all_types() -> list[dict[str, Any]]:
    all_items = db.session.query(TypPrzegladu).order_by(TypPrzegladu.typ).all()
    return [i.to_dict() for i in all_items]


@inspections_api.route("/types", methods=["POST"])
def create_type() -> dict[str, Any]:
    return insert(table=TypPrzegladu, values=request.form)


@inspections_api.route("/types/<type_id>", methods=["DELETE"])
def delete_type(type_id: int) -> Response:
    return delete_by_id(table=TypPrzegladu, id=type_id)


@inspections_api.route("/causes", methods=["GET"])
def get_cause() -> dict[str, Any]:
    return select_by_page(table=PowodPrzegladu, orderby=PowodPrzegladu.id)


@inspections_api.route("/causes", methods=["POST"])
def create_cause() -> dict[str, Any]:
    return insert(table=PowodPrzegladu, values=request.form)


@inspections_api.route("/causes/<cause_id>", methods=["DELETE"])
def delete_cause(cause_id: int) -> Response:
    return delete_by_id(table=PowodPrzegladu, id=cause_id)


@inspections_api.route("/requests", methods=["GET"])
def all_requests() -> list[dict[str, Any]]:
    return select_by_page(
        table=ZgloszeniePrzegladu, orderby=ZgloszeniePrzegladu.data
    )


@inspections_api.route("/requests", methods=["POST"])
def create_request() -> dict[str, Any]:
    return insert(table=ZgloszeniePrzegladu, values=request.form)


@inspections_api.route("/requests/<request_id>", methods=["DELETE"])
def delete_request(request_id: int) -> Response:
    return delete_by_id(table=ZgloszeniePrzegladu, id=request_id)


def insert(table: Any, values: Mapping[str, Any]) -> dict[str, Any]:
    item: SerializedBase = table(**values)
    db.session.add(item)
    db.session.commit()
    return item.to_dict()


def select_by_page(table: Any, orderby: Any) -> list[dict[str, Any]]:
    page: int = int(request.args.get("page", 1))
    page_size: int = int(request.args.get("page-size", 20))
    idx = page * page_size
    all_items = db.session.query(table).order_by(orderby)
    return [i.to_dict() for i in all_items[idx - page_size : idx]]


def delete_by_id(table: Any, id: int) -> Response:
    to_delete = db.session.query(table).where(table.id == id).one()
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        return jsonify({"message": errorMessage(err.args[0])})
    return jsonify({"message": "Obiekt pomyślnie usunięty"})


ERROR_TABLE = re.compile(r'relation "([^"]+)"|from table "([^"]+)"')
ERROR_ITEM = re.compile(r"Failing row contains \((\d+),")


def errorMessage(error):
    table = ERROR_TABLE.findall(error)[0]
    if table[0] != "":
        item_id = ERROR_ITEM.findall(error)[0]
        return f"Nie można usunąć obiektu - odwołuje się do niego obiekt o ID: {item_id} z tabeli '{table[0]}'"
    return f"Nie można usunąć obiektu - odwołuje się do niego obiekt z tabeli '{table[1]}'"
