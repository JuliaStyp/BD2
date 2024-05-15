import os

import click
from flask import Flask

from project.db import db, init_db
from project.routes import auth_bp, inspections_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"]
# "postgresql://postgres:postgres@localhost:5432/postgres"
app.register_blueprint(auth_bp)
app.register_blueprint(inspections_bp)

db.init_app(app)


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
