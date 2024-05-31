from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy.exc import IntegrityError
from project.db import db, Serwisant
from project.forms.service_form import ServiceForm
from project.utils import login_required, admin_required


service_bp = Blueprint("service_bp", __name__, url_prefix="/service")


@service_bp.route("/")
@login_required
def service():
    services = db.session.execute(db.select(Serwisant).order_by(Serwisant.id)).scalars()
    return render_template("service/service.html", services=services)


@service_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_service():
    context = {}
    if request.method == "POST":
        form = ServiceForm(request.form)
        if form.validate():
            new_service = Serwisant(
                nazwa=form.name.data,
                nr_telefonu=form.phone_number.data,
                adres_mail=form.mail.data,
            )
            db.session.add(new_service)
            db.session.commit()
            flash("Pomyślnie dodano serwisanta", "success")
            return redirect(url_for("service_bp.service"))
    else:
        form = ServiceForm()

    context["form"] = form
    return render_template("service/create_service.html", **context)


@service_bp.route("/delete/<id>", methods=["POST"])
@login_required
@admin_required
def delete_service(id):
    try:
        service = db.session.query(Serwisant).filter_by(id=id).first()
        db.session.delete(service)
        db.session.commit()
        flash("Pomyślnie usunięto serwisanta", "success")
    except IntegrityError:
        flash(
            "Nie można usunąć serwisanta, gdyż jest on wykorzystywany przez inne obiekty.",
            "error",
        )
    except:
        flash("Ups, coś poszło nie tak")
    return redirect(url_for("service_bp.service"))
