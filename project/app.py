import os

import click
from flask import Flask, session

from db import db, init_db
from routes.auth import auth_bp
from routes.index import index_bp
from routes.repairs import repairs_bp
from routes.service import service_bp

is_logged_in = False
is_admin = False

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"]
# "postgresql://postgres:postgres@localhost:5432/postgres"
app.secret_key = 'random_string_of_characters'

app.register_blueprint(auth_bp)
app.register_blueprint(index_bp)
app.register_blueprint(repairs_bp)
app.register_blueprint(service_bp)

db.init_app(app)


@app.context_processor
def inject_login_status():
    if 'user_id' in session:
        user_id = session['user_id']
        role = session['role']
        user_name = session['user_name']
        logged_in = True
    else:
        user_id = None
        role = None
        user_name = None
        logged_in = False
    return dict(logged_in=logged_in, user_id=user_id, role=role, user_name=user_name)


@click.group()
def cli() -> None:
    pass


@cli.command("run")
def run() -> None:
    app.run(debug=True)


@cli.command("init-db")
def initdb() -> None:
    init_db()


if __name__ == "__main__":
    cli()
