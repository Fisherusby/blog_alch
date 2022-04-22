from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from .db import db


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/my_db_flask_alch'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    from flaskblog.blueprints import bp_auth, bp_blog, bp_error
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_blog)
    app.register_blueprint(bp_error)


    db.init_app(app)
    migrate = Migrate(app, db)

    return app

