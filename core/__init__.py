import os

from flask import Flask
from flask_bootstrap import Bootstrap

from core import blueprints
from core.db import db


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:////tmp/test.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = bool(
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", 1)
    )

    # Secret key init -- NEED REWORK!!!
    app.secret_key = os.getenv("SECRET_KEY", b'_5#y2L"F4Q8z\n\xec]/')

    # Register all blueprints

    app.register_blueprint(blueprints.bp_auth)
    app.register_blueprint(blueprints.bp_blog)
    app.register_blueprint(blueprints.bp_error)

    # Database init
    db.init_app(app)

    return app
