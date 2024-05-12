import click
from dotenv import load_dotenv

import db

load_dotenv()


@click.group()
def cli() -> None:
    pass


@cli.command("init-db")
def initdb() -> None:
    db.init()


if __name__ == "__main__":
    cli()
