from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from project.db import db, Rola, Uzytkownik
from project.forms import UzytkownikForm, RolaForm

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/")
def auth():
    users = db.session.execute(db.select(Uzytkownik).order_by(Uzytkownik.id)).scalars()
    return render_template("auth/auth.html", users=users)


@auth_bp.route("/register", methods=["GET", "POST"])
def user_create():
    form = UzytkownikForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = Uzytkownik(
            rola_fk=form.rola_fk.data,
            imie=form.imie.data,
            nazwisko=form.nazwisko.data,
            email=form.email.data,
            numer_tel=form.numer_tel.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        session['flash_message'] = 'Pomyślnie dodano użytkownika'
        return redirect(url_for('auth_bp.auth'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/delete/<int:id>', methods=['GET'])
def user_delete(id):
    user = db.session.query(Uzytkownik).filter_by(id=id).first()
    if not user:
        session['flash_message'] = 'Nie znaleziono użytkownika o podanym ID.'
        return redirect(url_for('auth_bp.auth'))

    else:
        try:
            db.session.delete(user)
            db.session.commit()
            session['flash_message'] = 'Użytkownik został pomyślnie usunięty.'
        except:
            db.session.rollback()
            session['flash_message'] = \
                'Nie można usunąć Użytkownika, ponieważ jest używany jako klucz obcy w innych tabelach.'
        return redirect(url_for('auth_bp.auth'))


@auth_bp.route('/roles', methods=['GET'])
def roles():
    role_list = db.session.execute(db.select(Rola).order_by(Rola.id)).scalars()
    return render_template("auth/role.html", roles=role_list)


@auth_bp.route('/roles/create', methods=['GET', 'POST'])
def role_create():
    form = RolaForm(request.form)
    if request.method == 'POST' and form.validate():
        new_role = Rola(
            rola=form.rola.data
        )
        db.session.add(new_role)
        db.session.commit()
        session['flash_message'] = 'Pomyślnie dodano rolę'
        return redirect(url_for('auth_bp.roles'))
    return render_template('auth/create_role.html', form=form)


@auth_bp.route('/roles/delete/<int:id>', methods=['GET'])
def role_delete(id):
    rola = db.session.query(Rola).filter_by(id=id).first()
    if not rola:
        session['flash_message'] = 'Nie znaleziono roli o podanym ID.'
        return redirect(url_for('auth_bp.roles'))

    else:
        try:
            db.session.delete(rola)
            db.session.commit()
            session['flash_message'] = 'Rola została pomyślnie usunięta.'
        except:
            db.session.rollback()
            session['flash_message'] = \
                'Nie można usunąć Roli, ponieważ jest używana jako klucz obcy w innych tabelach.'
        return redirect(url_for('auth_bp.roles'))


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
            session['logged_in'] = True
            if user.rola_fk == 1:
                session['is_admin'] = True
            else:
                session['is_admin'] = False
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



