from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError

from project.db import (
    db,
    ElementInfrastruktury,
    Lokalizacja,
    Obiekt,
    TypInfrastruktury,
    StatusElementu,
)
from project.forms import LocationForm, ObjectForm, TypeForm, StatusForm, ElementForm

infr_bp = Blueprint("infr_bp", __name__, url_prefix="/infrastructure")


@infr_bp.route("/")
def infrastructure():
    element_list = db.session.execute(
        db.select(ElementInfrastruktury).order_by(ElementInfrastruktury.id)
    ).scalars()
    return render_template("infrastructure/infrastructure.html", elements=element_list)


@infr_bp.route("/create", methods=["GET", "POST"])
def create_element():
    context = {}
    if request.method == "POST":
        print("post")
        form = ElementForm(request.form)
        if form.validate():
            new_location = ElementInfrastruktury(
                typ=form.typ.data,
                lokalizacja=form.lokalizacja.data,
                obiekt=form.obiekt.data,
                status=form.status.data,
                opis=form.opis.data,
                max_interwal=form.max_interwal.data,
            )
            db.session.add(new_location)
            db.session.commit()
            session["flash_message"] = "Pomyślnie dodano element"
            flash("Pomyślnie dodano element")
            return redirect(url_for("infr_bp.infrastructure"))
    else:
        form = ElementForm()
    context["form"] = form

    return render_template("infrastructure/create_element.html", **context)


@infr_bp.route("/delete/<int:id>", methods=["GET"])
def delete_element(id):
    location = db.session.query(ElementInfrastruktury).filter_by(id=id).first()
    if not location:
        flash("Nie znaleziono elementu infrastruktury o podanym ID.", "error")
        return redirect(url_for("infr_bp.infrastructure"))

    else:
        try:
            db.session.delete(location)
            db.session.commit()
            session["flash_message"] = (
                "Element infrastruktury został pomyślnie usunięty."
            )
        except IntegrityError:
            db.session.rollback()
            session["flash_message"] = (
                "Nie można usunąć elementu, ponieważ jest używany jako klucz obcy w innych tabelach."
            )
        return redirect(url_for("infr_bp.infrastructure"))


@infr_bp.route("/locations", methods=["GET", "POST"])
def locations():
    location_list = db.session.execute(
        db.select(Lokalizacja).order_by(Lokalizacja.id)
    ).scalars()
    return render_template("infrastructure/locations.html", locations=location_list)


@infr_bp.route("/locations/create", methods=["GET", "POST"])
def create_location():
    context = {}
    if request.method == "POST":
        form = LocationForm(request.form)
        if form.validate():
            new_location = Lokalizacja(
                szerokosc_geo=form.szerokosc_geo.data,
                dlugosc_geo=form.dlugosc_geo.data,
                nazwa_miejsca=form.nazwa_miejsca.data,
            )
            db.session.add(new_location)
            db.session.commit()
            flash("Pomyślnie dodano lokalizację")
            return redirect(url_for("infr_bp.locations"))
    else:
        form = LocationForm()
    context["form"] = form

    return render_template("infrastructure/create_location.html", **context)


@infr_bp.route("/locations/delete/<int:id>", methods=["GET"])
def delete_location(id):
    location = db.session.query(Lokalizacja).filter_by(id=id).first()
    if not location:
        flash("Nie znaleziono lokalizacji o podanym ID.", "error")
        return redirect(url_for("infr_bp.locations"))

    else:
        try:
            db.session.delete(location)
            db.session.commit()
            session["flash_message"] = "Lokalizacja została pomyślnie usunięta."
        except IntegrityError:
            db.session.rollback()
            session["flash_message"] = (
                "Nie można usunąć lokalizacji, ponieważ jest używana jako klucz obcy w innych tabelach."
            )
        return redirect(url_for("infr_bp.locations"))


@infr_bp.route("/objects", methods=["GET", "POST"])
def objects():
    object_list = db.session.execute(db.select(Obiekt).order_by(Obiekt.id)).scalars()
    return render_template("infrastructure/objects.html", objects=object_list)


@infr_bp.route("/objects/create", methods=["GET", "POST"])
def create_object():
    context = {}
    if request.method == "POST":
        form = ObjectForm(request.form)
        if form.validate():
            new_object = Obiekt(typ=form.typ.data, do_uzytku=form.do_uzytku.data)
            db.session.add(new_object)
            db.session.commit()
            return redirect(url_for("infr_bp.objects"))
    else:
        form = ObjectForm()
    context["form"] = form

    return render_template("infrastructure/create_object.html", **context)


@infr_bp.route("/objects/delete/<int:id>", methods=["GET"])
def delete_object(id):
    obj = db.session.query(Obiekt).filter_by(id=id).first()
    if not obj:
        session["flash_message"] = "Nie znaleziono obiektu o podanym ID."
        return redirect(url_for("infr_bp.objects"))

    else:
        try:
            db.session.delete(obj)
            db.session.commit()
            session["flash_message"] = "Obiekt została pomyślnie usunięta."
        except IntegrityError:
            db.session.rollback()
            session["flash_message"] = (
                "Nie można usunąć obiektu, ponieważ jest używany jako klucz obcy w innych tabelach."
            )
        return redirect(url_for("infr_bp.objects"))


@infr_bp.route("/types", methods=["GET", "POST"])
def types():
    type_list = db.session.execute(
        db.select(TypInfrastruktury).order_by(TypInfrastruktury.id)
    ).scalars()
    return render_template("infrastructure/types.html", types=type_list)


@infr_bp.route("/types/create", methods=["GET", "POST"])
def create_type():
    context = {}
    if request.method == "POST":
        form = TypeForm(request.form)
        if form.validate():
            new_type = TypInfrastruktury(typ=form.typ.data)
            db.session.add(new_type)
            db.session.commit()
            flash("Pomyślnie dodano typ infrastruktury")
            return redirect(url_for("infr_bp.types"))
    else:
        form = TypeForm()
    context["form"] = form

    return render_template("infrastructure/create_type.html", **context)


@infr_bp.route("/types/delete/<int:id>", methods=["GET"])
def delete_type(id):
    typ = db.session.query(TypInfrastruktury).filter_by(id=id).first()
    if not typ:
        flash("Nie znaleziono typu o podanym ID.", "error")
        return redirect(url_for("infr_bp.types"))

    else:
        try:
            db.session.delete(typ)
            db.session.commit()

            session["flash_message"] = "Typ został pomyślnie usunięty"
        except IntegrityError:
            db.session.rollback()
            session["flash_message"] = (
                "Nie można usunąć typu, ponieważ jest używany jako klucz obcy w innych tabelach."
            )
        return redirect(url_for("infr_bp.types"))


@infr_bp.route("/statuses", methods=["GET", "POST"])
def statuses():
    status_list = db.session.execute(
        db.select(StatusElementu).order_by(StatusElementu.id)
    ).scalars()
    return render_template("infrastructure/statuses.html", statuses=status_list)


@infr_bp.route("/statuses/create", methods=["GET", "POST"])
def create_status():
    context = {}
    if request.method == "POST":
        form = StatusForm(request.form)
        if form.validate():
            new_status = StatusElementu(status=form.status.data)
            db.session.add(new_status)
            db.session.commit()
            flash("Pomyślnie dodano status elementu")
            return redirect(url_for("infr_bp.statuses"))
    else:
        form = StatusForm()
    context["form"] = form

    return render_template("infrastructure/create_status.html", **context)


@infr_bp.route("/statuses/delete/<int:id>", methods=["GET"])
def delete_status(id):
    status = db.session.query(StatusElementu).filter_by(id=id).first()
    if not status:
        flash("Nie znaleziono statusu o podanym ID.", "error")
        return redirect(url_for("infr_bp.statuses"))

    else:
        try:
            db.session.delete(status)
            db.session.commit()
            session["flash_message"] = "Status został pomyślnie usunięty"
        except IntegrityError:
            db.session.rollback()
            session["flash_message"] = (
                "Nie można usunąć statusu, ponieważ jest używany jako klucz obcy w innych tabelach."
            )
        return redirect(url_for("infr_bp.statuses"))
