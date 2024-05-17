from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from project.db import db, Rola, Uzytkownik

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/")
def auth():
    users = db.session.execute(db.select(Uzytkownik).order_by(Uzytkownik.id)).scalars()
    return render_template("auth/auth.html", users=users)


@auth_bp.route("/register", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = Uzytkownik(
            # id=request.form["id"],
            rola_fk=request.form["rola_fk"],
            imie=request.form["imie"],
            nazwisko=request.form["nazwisko"],
            email=request.form["email"],
            numer_tel=request.form["numer_tel"],
        )
        user.set_password(request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth_bp.auth"))

    return render_template("auth/register.html")


@auth_bp.route("/role", methods=["GET", "POST"])
def role_create():
    if request.method == "POST":
        role = Rola(rola=request.form["rola"])
        db.session.add(role)
        db.session.commit()
        return redirect(url_for("auth_bp.auth"))

    return render_template("auth/role.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Example logic for authentication (replace with your actual logic)
        user = db.session.query(Uzytkownik).filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # Successful login, redirect to home page
            role = db.session.query(Rola).filter_by(id=user.rola_fk).first()

            session['user_id'] = user.id
            session['role'] = user.rola_fk
            session['user_name'] = user.imie
            session['role_name'] = role.rola if role else "Unknown"
            return redirect(url_for("auth_bp.auth"))
        else:
            # Invalid credentials, show error message
            error = "Invalid email or password"
            return render_template("auth/login.html", error=error)

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    # Clear session data (log out user)
    session.clear()
    return redirect(url_for("auth_bp.login"))



