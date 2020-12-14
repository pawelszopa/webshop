from flask import Flask, g


def create_app():
    alegrosz = Flask(__name__)

    from .views import bp_main
    alegrosz.register_blueprint(bp_main)

    # this decorator before it will be closed ctr c this function will happened
    @alegrosz.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, "_database", None)
        if db is not None:
            db.close()

    return alegrosz
