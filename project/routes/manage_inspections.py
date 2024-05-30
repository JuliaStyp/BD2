from flask import Blueprint, render_template

manage_inspections_bp = Blueprint(
    "manage_inspections", __name__, url_prefix="/inspections"
)


@manage_inspections_bp.route("/", methods=["GET"])
def root() -> str:
    return render_template("inspections/inspections_root.html")


@manage_inspections_bp.route("/inspections", methods=["GET"])
def inspections() -> str:
    return render_template("inspections/inspections.html")


@manage_inspections_bp.route("/types", methods=["GET"])
def types() -> str:
    return render_template("inspections/inspection_types.html")


@manage_inspections_bp.route("/causes", methods=["GET"])
def causes() -> str:
    return render_template("inspections/inspection_causes.html")


@manage_inspections_bp.route("/requests", methods=["GET"])
def requests() -> str:
    return render_template("inspections/inspection_requests.html")
