from typing import Any, Mapping

from flask import Blueprint, request

from project.db import db, Przeglad, TypPrzegladu, PowodPrzegladu, ZgloszeniePrzegladu
from project.db.models import SerializedBase

inspections_bp = Blueprint("inspections_bp", __name__, url_prefix="/api/inspections")


@inspections_bp.route("/", methods=["GET"])
def all_inspections() -> list[dict[str, Any]]:
    return select_by_page(table=Przeglad, orderby=Przeglad.data_rozpoczecia)


@inspections_bp.route("/", methods=["POST"])
def create_inspection() -> dict[str, Any]:
    return insert(table=Przeglad, values=request.form)


@inspections_bp.route("/<inspection_id>", methods=["DELETE"])
def delete_inspection(inspection_id: int) -> str:
    return delete_by_id(table=Przeglad, id=inspection_id)


@inspections_bp.route("/types", methods=["GET"])
def all_types() -> list[dict[str, Any]]:
    all_items = db.session.query(TypPrzegladu).order_by(TypPrzegladu.typ).all()
    return [i.to_dict() for i in all_items]


@inspections_bp.route("/types", methods=["POST"])
def create_type() -> dict[str, Any]:
    return insert(table=TypPrzegladu, values=request.form)


@inspections_bp.route("/types/<type_id>", methods=["DELETE"])
def delete_type(type_id: int) -> str:
    return delete_by_id(table=TypPrzegladu, id=type_id)


@inspections_bp.route("/causes/<cause_id>", methods=["GET"])
def get_cause(cause_id: int) -> dict[str, Any]:
    cause = db.session.query(PowodPrzegladu).where(PowodPrzegladu.id == cause_id).one()
    return cause.to_dict()


@inspections_bp.route("/causes", methods=["POST"])
def create_cause() -> dict[str, Any]:
    return insert(table=PowodPrzegladu, values=request.form)


@inspections_bp.route("/causes/<cause_id>", methods=["DELETE"])
def delete_cause(cause_id: int) -> str:
    return delete_by_id(table=PowodPrzegladu, id=cause_id)


@inspections_bp.route("/requests", methods=["GET"])
def all_requests() -> list[dict[str, Any]]:
    return select_by_page(table=ZgloszeniePrzegladu, orderby=ZgloszeniePrzegladu.data)


@inspections_bp.route("/requests", methods=["POST"])
def create_request() -> dict[str, Any]:
    return insert(table=ZgloszeniePrzegladu, values=request.form)


@inspections_bp.route("/requests/<request_id>", methods=["DELETE"])
def delete_request(request_id: int) -> str:
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


def delete_by_id(table: Any, id: int) -> str:
    to_delete = db.session.query(table).where(table.id == id).one()
    db.session.delete(to_delete)
    db.session.commit()
    return "Deleted"
