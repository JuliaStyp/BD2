from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from project.db import (
    db,
    PowodNaprawy,
    ZgloszenieNaprawy,
    Naprawa,
    Serwisant,
    ElementInfrastruktury,
    Przeglad,
)
from project.forms import ReportForm
from project.utils import login_required


reports_bp = Blueprint("reports_bp", __name__, url_prefix="/reports")


@reports_bp.route("", methods=["GET", "POST"])
@login_required
def reports():
    if request.method == "POST":
        form = ReportForm(request.form)
        if form.validate():
            if form.type.data == "Naprawy":
                return create_repairs_report(form.date_start.data, form.date_end.data)
            else:
                return create_inspections_report(
                    form.date_start.data, form.date_end.data
                )
    else:
        form = ReportForm()

    return render_template("reports/reports.html", form=form)


def create_repairs_report(date_start, date_end):
    repairs = (
        db.session.query(Naprawa)
        .where(date_start <= Naprawa.data_rozpoczecia)
        .where(Naprawa.data_rozpoczecia <= date_end)
        .order_by(Naprawa.id.desc())
        .all()
    )
    return render_template(
        "reports/repairs_raport.html",
        repairs=repairs,
        date_start=date_start,
        date_end=date_end,
    )


def create_inspections_report(date_start, date_end):
    inspections = (
        db.session.query(Przeglad)
        .where(date_start <= Przeglad.data_rozpoczecia)
        .where(Przeglad.data_rozpoczecia <= date_end)
        .order_by(Przeglad.id.desc())
        .all()
    )
    return render_template(
        "reports/inspections_raport.html",
        inspections=inspections,
        date_start=date_start,
        date_end=date_end,
    )
