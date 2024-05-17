from flask import Blueprint, render_template

manage_inspections_bp = Blueprint(
    "manage_inspections", __name__, url_prefix="/manage-inspections"
)


@manage_inspections_bp.route("/", methods=["GET"])
def root() -> str:
    return render_template("inspections_root.html")


@manage_inspections_bp.route("/inspections", methods=["GET"])
def inspections() -> str:
    return render_template("inspections.html")


@manage_inspections_bp.route("/types", methods=["GET"])
def types() -> str:
    return render_template("inspection_types.html")


@manage_inspections_bp.route("/causes", methods=["GET"])
def causes() -> str:
    return render_template("inspection_causes.html")


@manage_inspections_bp.route("/requests", methods=["GET"])
def requests() -> str:
    return render_template("inspection_requests.html")
