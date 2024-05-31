from flask import Blueprint, render_template

from project.forms.inspections_forms import (
    InspectionsForm,
    TypesForm,
    CausesForm,
    RequestsForm,
)
from project.utils import admin_required, login_required

inspections_ui = Blueprint("inspections_ui", __name__, url_prefix="/inspections")


@inspections_ui.route("/", methods=["GET"])
@login_required
def root() -> str:
    return render_template("inspections/inspections_root.html")


@inspections_ui.route("/inspections", methods=["GET"])
@login_required
def inspections() -> str:
    return render_template("inspections/inspections_list.html")


@inspections_ui.route("/inspections/create", methods=["GET"])
@login_required
@admin_required
def inspections_create() -> str:
    form = InspectionsForm()
    return render_template("/inspections/form_inspections.html", form=form)


@inspections_ui.route("/types", methods=["GET"])
@login_required
def types() -> str:
    return render_template("inspections/inspection_types.html")


@inspections_ui.route("/types/create", methods=["GET"])
@login_required
@admin_required
def types_create() -> str:
    form = TypesForm()
    return render_template("/inspections/form_types.html", form=form)


@inspections_ui.route("/causes", methods=["GET"])
@login_required
def causes() -> str:
    return render_template("inspections/inspection_causes.html")


@inspections_ui.route("/causes/create", methods=["GET"])
@login_required
@admin_required
def causes_create() -> str:
    form = CausesForm()
    return render_template("/inspections/form_causes.html", form=form)


@inspections_ui.route("/requests", methods=["GET"])
@login_required
def requests() -> str:
    return render_template("inspections/inspection_requests.html")


@inspections_ui.route("/requests/create", methods=["GET"])
@login_required
@admin_required
def requests_create() -> str:
    form = RequestsForm()
    return render_template("/inspections/form_requests.html", form=form)
