import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from project.db.models import Uzytkownik, Rola

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite db, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"]
# "postgresql://postgres:postgres@localhost:5432/postgres"
db.init_app(app)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route("/auth")
def auth():
    users = db.session.execute(db.select(Uzytkownik).order_by(Uzytkownik.id)).scalars()
    return render_template("auth.html", users=users)


@app.route("/auth/register", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = Uzytkownik(
            id=request.form["id"],
            rola_fk=request.form["rola_fk"],
            imie=request.form["imie"],
            nazwisko=request.form["nazwisko"],
            email=request.form["email"],
            numer_tel=request.form["numer_tel"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth"))

    return render_template("register.html")


@app.route("/auth/role", methods=["GET", "POST"])
def role_create():
    if request.method == "POST":
        role = Rola(
            id=request.form["id"],
            rola=request.form["rola"]
        )
        db.session.add(role)
        db.session.commit()
        return redirect(url_for("auth"))

    return render_template("role.html")


if __name__ == '__main__':
    app.run(debug=True)
