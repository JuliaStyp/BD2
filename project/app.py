import os

from flask import Flask
from routes.auth import auth_bp
from project.db.database import db

# create the extension

# create the app
app = Flask(__name__)
# configure the SQLite db, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"]
# "postgresql://postgres:postgres@localhost:5432/postgres"
db.init_app(app)

app.register_blueprint(auth_bp)


if __name__ == '__main__':
    app.run(debug=True)
