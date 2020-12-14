from flask import Flask


def create_app():
    alegrosz = Flask(__name__)
    from .views import bp_main
    alegrosz.register_blueprint(bp_main)

    return alegrosz
