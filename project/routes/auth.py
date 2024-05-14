from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from db import db, Rola, Uzytkownik

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
        user.set_password(request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth_bp.auth"))

    return render_template("register.html")


@auth_bp.route("/role", methods=["GET", "POST"])
def role_create():
    if request.method == "POST":
        role = Rola(id=request.form["id"], rola=request.form["rola"])
        db.session.add(role)
        db.session.commit()
        return redirect(url_for("auth_bp.auth"))

    return render_template("role.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Example logic for authentication (replace with your actual logic)
        user = db.session.query(Uzytkownik).filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # Successful login, redirect to home page
            session['user_id'] = user.id
            session['role'] = user.rola_fk
            return redirect(url_for("auth_bp.auth"))
        else:
            # Invalid credentials, show error message
            error = "Invalid email or password"
            return render_template("login.html", error=error)

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    # Clear session data (log out user)
    session.clear()
    return redirect(url_for("auth_bp.login"))


@auth_bp.context_processor
def inject_login_status():
    if 'user_id' in session:
        user_id = session['user_id']
        role = session['role']
        logged_in = True
    else:
        user_id = None
        role = None
        logged_in = False
    return dict(logged_in=logged_in, user_id=user_id, role=role)
