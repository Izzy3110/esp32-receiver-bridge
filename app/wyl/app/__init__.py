from flask import Flask
from wyl.app.blueprints.data import bp_data


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_data)
    return app
