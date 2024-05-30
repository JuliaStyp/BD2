from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from project.db import db, PowodNaprawy, ZgloszenieNaprawy, Naprawa, Serwisant, ElementInfrastruktury, \
                        Przeglad
from project.forms import RepairReasonForm, RepairNeedReportForm, RepairForm

repairs_bp = Blueprint("repairs_bp", __name__, url_prefix="/repairs")

ITEMS_PER_PAGE = 20

# REPAIR REASONS

@repairs_bp.route("/repair-reasons/create", methods=["GET", "POST"])
def create_repair_reason():
    context = {}
    if request.method == "POST":
        form = RepairReasonForm(request.form)
        set_form_choices([(form.inspection_id, Przeglad),
                          (form.repair_need_report_id, ZgloszenieNaprawy)])
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
        set_form_choices([(form.inspection_id, Przeglad),
                          (form.repair_need_report_id, ZgloszenieNaprawy)])

    context['form'] = form

    return render_template("repairs/create_repair_reason.html", **context)


@repairs_bp.route("/repair-reasons", methods=["GET"])
@repairs_bp.route("/repair-reasons/<int:page>", methods=["GET"])
def list_repair_reasons(page=1):
    context = {}
    query = db.session.query(PowodNaprawy)
    reasons = db.paginate(query, page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    if reasons.pages < page:
        reasons = db.paginate(query, page=reasons.pages, per_page=ITEMS_PER_PAGE, error_out=False)
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

@repairs_bp.route("/repair-need-reports/<int:page>", methods=["GET"])
@repairs_bp.route("/repair-need-reports", methods=["GET"])
def list_reports(page=1):
    context = {}
    query = db.session.query(ZgloszenieNaprawy)
    reports = db.paginate(query, page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    if reports.pages < page:
        reports = db.paginate(query, page=reports.pages, per_page=ITEMS_PER_PAGE, error_out=False)
    context['reports'] = reports

    return render_template("repairs/list_reports.html", **context)


@repairs_bp.route("/repair-need-reports/create", methods=["GET", "POST"])
def create_report():
    context = {}
    if request.method == "POST":
        form = RepairNeedReportForm(request.form)
        set_form_choices([(form.element_id, ElementInfrastruktury)])
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
        set_form_choices([(form.element_id, ElementInfrastruktury)])
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
@repairs_bp.route("/<int:page>", methods=["GET"])
def list_repairs(page=1):
    context = {}
    query = db.session.query(Naprawa)
    repairs = db.paginate(query, page=page, per_page=ITEMS_PER_PAGE, error_out=False)
    if repairs.pages < page:
        repairs = db.paginate(query, page=repairs.pages, per_page=ITEMS_PER_PAGE, error_out=False)
    context['repairs'] = repairs

    return render_template("repairs/list_repairs.html", **context)


@repairs_bp.route("/create", methods=["GET", "POST"])
def create_repair():
    context = {}
    if request.method == "POST":
        form = RepairForm(request.form)
        set_form_choices([(form.reason_id, PowodNaprawy),
                          (form.maintainer_id, Serwisant),
                          (form.element_id, ElementInfrastruktury)])
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
        set_form_choices([(form.reason_id, PowodNaprawy),
                          (form.maintainer_id, Serwisant),
                          (form.element_id, ElementInfrastruktury)])
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
    return redirect(url_for("repairs_bp.list_repairs"))


def set_form_choices(forms_fields_and_models: list):
    for form_field, model in forms_fields_and_models:
        objects = db.session.query(model).order_by(model.id.desc()).all()
        form_field.choices = [obj.id for obj in objects]


# GET RENDERED DATA

def get_object_by_id_with_status(model, id):
    object = db.session.query(model).filter_by(id=id).first()
    if object is not None:
        status = 'ok'
    else:
        status = 'error'
    return (object, status)

@repairs_bp.route("/get-data/maintainers/<id>", methods=['GET'])
def get_rendered_maintainer(id):
    maintainer, status = get_object_by_id_with_status(Serwisant, id)
    rendered_data = render_template('repairs/maintainer_data.html', maintainer=maintainer)
    return jsonify({'status': status,
                    'data': rendered_data})


@repairs_bp.route("/get-data/repair-reasons/<id>", methods=['GET'])
def get_rendered_repair_reason(id):
    repair_reason, status = get_object_by_id_with_status(PowodNaprawy, id)
    rendered_data = render_template('repairs/repair_reason_data.html', reason=repair_reason)
    return jsonify({'status': status,
                    'data': rendered_data})


@repairs_bp.route("/get-data/elements/<id>", methods=['GET'])
def get_rendered_element(id):
    element, status = get_object_by_id_with_status(ElementInfrastruktury, id)
    rendered_data = render_template('repairs/element_data.html', element=element)
    return jsonify({'status': status,
                    'data': rendered_data})


@repairs_bp.route("/get-data/inspections/<id>", methods=['GET'])
def get_rendered_inspection(id):
    inspection, status = get_object_by_id_with_status(Przeglad, id)
    rendered_data = render_template('repairs/inspection_data.html', inspection=inspection)
    return jsonify({'status': status,
                    'data': rendered_data})


@repairs_bp.route("/get-data/repair-need-reports/<id>", methods=['GET'])
def get_rendered_repair_need_report(id):
    report, status = get_object_by_id_with_status(ZgloszenieNaprawy, id)
    rendered_data = render_template('repairs/report_data.html', report=report)
    return jsonify({'status': status,
                    'data': rendered_data})
