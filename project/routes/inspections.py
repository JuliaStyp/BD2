from typing import Any

from flask import Blueprint, request

from project.db import db, Przeglad, TypPrzegladu

inspections_bp = Blueprint("inspections_bp", __name__, url_prefix="/inspections")


@inspections_bp.route("/", methods=["GET"])
def get_inspections() -> list[dict[str, Any]]:
    page: int = request.args.get("page", 1)
    page_size: int = request.args.get("page-size", 20)
    idx = page * page_size
    all_inspections = db.session.query(Przeglad).order_by(Przeglad.data_rozpoczecia)[
        idx - page_size : idx
    ]
    return [i.to_dict() for i in all_inspections]


@inspections_bp.route("/", methods=["POST"])
def create_inspection() -> dict[str, Any]:
    inspection = Przeglad(**request.form)
    db.session.add(inspection)
    db.session.commit()
    return inspection.to_dict()


@inspections_bp.route("/types", methods=["GET"])
def get_type() -> list[dict[str, Any]]:
    all_types = db.session.query(TypPrzegladu).order_by(TypPrzegladu.typ).all()
    return [i.to_dict() for i in all_types]


@inspections_bp.route("/types", methods=["POST"])
def create_type() -> dict[str, Any]:
    inspection_type = TypPrzegladu(**request.form)
    db.session.add(inspection_type)
    db.session.commit()
    return inspection_type.to_dict()


@inspections_bp.route("/types/<type_id>", methods=["DELETE"])
def delete_type(type_id: int) -> str:
    to_delete = db.session.query(TypPrzegladu).where(TypPrzegladu.id == type_id).one()
    db.session.delete(to_delete)
    db.session.commit()
    return "Deleted"
