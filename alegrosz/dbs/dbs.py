import os
import _sqlite3

from flask import g



db_abspath = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(db_abspath, "..", "alegrosz.db")



def get_db():
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = _sqlite3.connect(db_path)

    return db
