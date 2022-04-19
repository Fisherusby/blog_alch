from .db import db
from . import create_app


def create_db():
    # Create all models as tables in DB
    app = create_app()
    with app.test_request_context():
        db.init_app(app)
        db.create_all()


def drop_db():
    # Drop all tables in DB
    app = create_app()
    with app.test_request_context():
        db.init_app(app)
        db.drop_all()
