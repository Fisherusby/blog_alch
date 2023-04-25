from core import create_app
from core.db import db


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


def add_in_db(add_data):
    # Add data in DB
    app = create_app()
    with app.test_request_context():
        db.init_app(app)
        if isinstance(add_data, list):
            for el in add_data:
                db.session.add(el)
        else:
            db.session.add(add_data)
        db.session.commit()
