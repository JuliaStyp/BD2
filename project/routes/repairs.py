from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import db, PowodNaprawy, ZgloszenieNaprawy, Naprawa
from forms import RepairReasonForm, RepairNeedReportForm, RepairForm

repairs_bp = Blueprint("repairs_bp", __name__, url_prefix="/repairs")


# REPAIR REASONS

@repairs_bp.route("/repair-reasons/create", methods=["GET", "POST"])
def create_repair_reason():
    context = {}
    if request.method == "POST":
        form = RepairReasonForm(request.form)
        if form.validate():
            new_repair_reason = PowodNaprawy(
                przeglad_id=form.inspection_id.data,
                zgloszenie_id=form.repair_need_report_id.data,
                priorytet=form.priority.data,
                uwagi=form.remarks.data,
            )
            db.session.add(new_repair_reason)
            db.session.commit()
            flash("Pomyślnie dodano powód naprawy")
            return redirect(url_for("repairs_bp.list_repair_reasons"))
    else:
        form = RepairReasonForm()
    context['form'] = form

    return render_template("repairs/create_repair_reason.html", **context)


@repairs_bp.route("/repair-reasons", methods=["GET"])
def list_repair_reasons():
    context = {}
    reasons = db.session.query(PowodNaprawy).all()
    context['reasons'] = reasons

    return render_template("repairs/list_repair_reasons.html", **context)


@repairs_bp.route("/repair-reasons/delete/<id>", methods=["POST"])
def delete_repair_reason(id):
    try:
        repair_reason = db.session.query(PowodNaprawy).filter_by(id=id).first()
        db.session.delete(repair_reason)
        db.session.commit()
        flash("Pomyślnie usunięto powód naprawy")
    except:
        flash("Ups, coś poszło nie tak")
    return redirect(url_for("repairs_bp.list_repair_reasons"))



# REAPIR NEED REPORTS

@repairs_bp.route("/repair-need-reports", methods=["GET"])
def list_reports():
    context = {}
    reports = db.session.query(ZgloszenieNaprawy).all()
    context['reports'] = reports

    return render_template("repairs/list_reports.html", **context)


@repairs_bp.route("/repair-need-reports/create", methods=["GET", "POST"])
def create_report():
    context = {}
    if request.method == "POST":
        form = RepairNeedReportForm(request.form)
        if form.validate():
            new_repair_reason = ZgloszenieNaprawy(
                element_id=form.element_id.data,
                data=form.date.data,
                zglaszajacy=form.reporting_person.data,
                uwagi=form.remarks.data
            )
            db.session.add(new_repair_reason)
            db.session.commit()
            flash("Pomyślnie dodano zgłoszenie potrzeby naprawy")
            return redirect(url_for("repairs_bp.list_reports"))
    else:
        form = RepairNeedReportForm()
    context['form'] = form

    return render_template("repairs/create_report.html", **context)


@repairs_bp.route("/repair-need-reports/delete/<id>", methods=["POST"])
def delete_report(id):
    try:
        repair_need_report = db.session.query(ZgloszenieNaprawy).filter_by(id=id).first()
        db.session.delete(repair_need_report)
        db.session.commit()
        flash("Pomyślnie usunięto zgłoszenie potrzeby naprawy")
    except:
        flash("Ups, coś poszło nie tak")
    return redirect(url_for("repairs_bp.list_reports"))


# REPAIRS

@repairs_bp.route("", methods=["GET"])
def list_repairs():
    context = {}
    repairs = db.session.query(Naprawa).all()
    context['repairs'] = repairs

    return render_template("repairs/list_repairs.html", **context)


@repairs_bp.route("/create", methods=["GET", "POST"])
def create_repair():
    context = {}
    if request.method == "POST":
        form = RepairForm(request.form)
        if form.validate():
            new_repair = Naprawa(
                powod_id=form.reason_id.data,
                serwisant_id=form.maintainer_id.data,
                element_id=form.element_id.data,
                data_rozpoczecia=form.date_start.data,
                data_zakonczenia=form.date_end.data,
                koszt=form.cost.data
            )
            db.session.add(new_repair)
            db.session.commit()
            flash("Pomyślnie dodano naprawę")
            return redirect(url_for("repairs_bp.list_repairs"))
    else:
        form = RepairForm()
    context['form'] = form

    return render_template("repairs/create_repair.html", **context)


@repairs_bp.route("/delete/<id>", methods=["POST"])
def delete_repair(id):
    try:
        repair = db.session.query(Naprawa).filter_by(id=id).first()
        db.session.delete(repair)
        db.session.commit()
        flash("Pomyślnie usunięto naprawę")
    except:
        flash("Ups, coś poszło nie tak")
    return redirect(url_for("repairs_bp.list_reports"))