from flask import Blueprint, render_template, request, redirect, url_for

from project.db import db, Rola, Uzytkownik

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/")
def auth():
    users = db.session.execute(db.select(Uzytkownik).order_by(Uzytkownik.id)).scalars()
    return render_template("auth.html", users=users)


@auth_bp.route("/register", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = Uzytkownik(
            id=request.form["id"],
            rola_fk=request.form["rola_fk"],
            imie=request.form["imie"],
            nazwisko=request.form["nazwisko"],
            email=request.form["email"],
            numer_tel=request.form["numer_tel"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth"))

    return render_template("register.html")


@auth_bp.route("/role", methods=["GET", "POST"])
def role_create():
    if request.method == "POST":
        role = Rola(id=request.form["id"], rola=request.form["rola"])
        db.session.add(role)
        db.session.commit()
        return redirect(url_for("auth"))

    return render_template("role.html")
