from flask import Blueprint, render_template, request, redirect, url_for

from project.db import db, ElementInfrastruktury, Lokalizacja, Obiekt, TypInfrastruktury, StatusElementu

infr_bp = Blueprint("infr_bp", __name__, url_prefix="/infrastructure")


@infr_bp.route("/")
def infrastructure():
    element_list = db.session.execute(db.select(ElementInfrastruktury).order_by(ElementInfrastruktury.id)).scalars()
    return render_template("infrastructure/infrastructure.html", elements=element_list)


@infr_bp.route("/locations", methods=["GET", "POST"])
def locations():
    location_list = db.session.execute(db.select(Lokalizacja).order_by(Lokalizacja.id)).scalars()
    return render_template("infrastructure/locations.html", locations=location_list)


@infr_bp.route("/objects", methods=["GET", "POST"])
def objects():
    object_list = db.session.execute(db.select(Obiekt).order_by(Obiekt.id)).scalars()
    return render_template("infrastructure/objects.html", objects=object_list)


@infr_bp.route("/types", methods=["GET", "POST"])
def types():
    type_list = db.session.execute(db.select(TypInfrastruktury).order_by(TypInfrastruktury.id)).scalars()
    return render_template("infrastructure/types.html", types=type_list)


@infr_bp.route("/statuses", methods=["GET", "POST"])
def statuses():
    status_list = db.session.execute(db.select(StatusElementu).order_by(StatusElementu.id)).scalars()
    return render_template("infrastructure/statuses.html", statuses=status_list)
