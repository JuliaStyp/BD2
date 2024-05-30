from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import desc
from project.db import db, Naprawa, Przeglad

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/")
def index():
    repairs = db.session.execute(
        db.select(Naprawa).order_by(desc(Naprawa.id)).limit(5)
    ).scalars()
    inspections = db.session.execute(
        db.select(Przeglad).order_by(desc(Przeglad.id)).limit(5)
    ).scalars()
    return render_template("index.html", repairs=repairs, inspections=inspections)
