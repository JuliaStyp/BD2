from flask import Blueprint, render_template, request, redirect, url_for, session
from project.db import db, PowodNaprawy
from project.forms import RepairReasonForm

repairs_bp = Blueprint("repairs_bp", __name__, url_prefix="/repairs")

@repairs_bp.route("/repair-reasons/create", methods=["GET", "POST"])
def create_repair_reason():
    context = {}
    if request.method == "POST":
        print('1')
        form = RepairReasonForm(request.form)
        if form.validate():
            print('2')
            new_repair_reason = PowodNaprawy(
                przeglad_id=form.inspection_id.data,
                zgloszenie_id=form.repair_need_report_id.data,
                priorytet=form.priority.data,
                uwagi=form.remarks.data,
            )
            db.session.add(new_repair_reason)
            db.session.commit()
            return redirect(url_for("repairs_bp.list_repair_reasons"))
    else:
        form = RepairReasonForm()
    context['form'] = form
    print(form.errors)
    return render_template("repairs/create_repair_reason.html", **context)


@repairs_bp.route("/repair-reasons", methods=["GET"])
def list_repair_reasons():
    return "<h1> Są naprawy robione </h1>"
