from flask import Blueprint, render_template

inspections_ui = Blueprint("inspections_ui", __name__, url_prefix="/inspections")


@inspections_ui.route("/", methods=["GET"])
def root() -> str:
    return render_template("inspections/inspections_root.html")


@inspections_ui.route("/inspections", methods=["GET"])
def inspections() -> str:
    return render_template("inspections/inspections_list.html")


@inspections_ui.route("/types", methods=["GET"])
def types() -> str:
    return render_template("inspections/inspection_types.html")


@inspections_ui.route("/causes", methods=["GET"])
def causes() -> str:
    return render_template("inspections/inspection_causes.html")


@inspections_ui.route("/requests", methods=["GET"])
def requests() -> str:
    return render_template("inspections/inspection_requests.html")
