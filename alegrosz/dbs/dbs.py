import os  # build in
import _sqlite3  # build in

from flask import g  # third party

#  import our

db_abspath = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(db_abspath, "..", "alegrosz.db")


# connection to db sometimes we have to be in different (views, logic)
# global var in flask  is use here
# database is name given by us None if it is not found then nothing
def get_db():
    db = getattr(g, "_database", None)
    # if it is None we need to provide abs path - redo in config
    if db is None:
        db = g._database = _sqlite3.connect(db_path)
    # first db then _sqlite3 g._database = _sqlite3.con and in new line db = g._data
    return db
#  important that there is only one connection with db (this is why we need getattr)

# after we  open db we need to close db
