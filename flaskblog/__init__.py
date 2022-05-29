from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from .db import db


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Secret key init -- NEED REWORK!!!
    app.secret_key = '>>> Insert your secret key <<<'b'_5#y2L"F4Q8z\n\xec]/'

    # Register all blueprints
    from .blueprints import bp_auth, bp_blog, bp_error
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_blog)
    app.register_blueprint(bp_error)

    # Database init
    db.init_app(app)
    migrate = Migrate(app, db)

    return app

