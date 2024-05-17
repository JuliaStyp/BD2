from flask import Blueprint, render_template, request, redirect, url_for, session
from project.db import db, Serwisant

service_bp = Blueprint("service_bp", __name__, url_prefix="/service")

@service_bp.route("/")
def service():
    services = db.session.execute(db.select(Serwisant).order_by(Serwisant.id)).scalars()
    return render_template("service/service.html", services=services)