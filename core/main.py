from flask import Flask
from flask_bootstrap import Bootstrap

from core import endpoints, settings
from core.db import db


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    Bootstrap(app)

    app.secret_key = settings.SECRET_KEY

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

    # Register all endpoints
    app.register_blueprint(endpoints.bp_auth)
    app.register_blueprint(endpoints.bp_blog)
    app.register_blueprint(endpoints.bp_error)

    # Database init
    db.init_app(app)

    return app
