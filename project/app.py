import os

import click
from flask import Flask, session

from project.db import db, init_db, clear_db
from project.routes import auth_bp, index_bp, inspections_bp, manage_inspections_bp


is_logged_in = False
is_admin = False

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"]
# "postgresql://postgres:postgres@localhost:5432/postgres"
app.secret_key = "random_string_of_characters"

app.register_blueprint(auth_bp)
app.register_blueprint(index_bp)
app.register_blueprint(inspections_bp)
app.register_blueprint(manage_inspections_bp)

db.init_app(app)


@app.context_processor
def inject_login_status():
    if "user_id" in session:
        user_id = session["user_id"]
        role = session["role"]
        role_name = session["role_name"]
        logged_in = True
    else:
        user_id = None
        role = None
        role_name = None
        logged_in = False
    return dict(logged_in=logged_in, user_id=user_id, role=role, role_name=role_name)


@click.group()
def cli() -> None:
    pass


@cli.command("run")
def run() -> None:
    app.run(debug=True)


@cli.command("init-db")
def initdb() -> None:
    init_db()


@cli.command("clear-db")
def cleardb() -> None:
    with app.app_context():
        clear_db()


if __name__ == "__main__":
    cli()
