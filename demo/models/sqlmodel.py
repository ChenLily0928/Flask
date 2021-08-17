import os
import sqlite3
from flask import g, Blueprint

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database\\temp.db")
execSql = Blueprint("execSql", __name__)


def create_tables(app):
    with app.app_context():
        db = connect_db()
        with app.open_resource("models\schema.sql", mode="r") as f:
            cursor = db.cursor()
            cursor.executescript(f.read())
        db.commit()


def connect_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
