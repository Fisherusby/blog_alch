from flaskblog.init_db import create_db, drop_db
from flaskblog.db import db
from flaskblog import create_app
from flaskblog.models import Category, User
from flaskblog.models.user import ADMIN, ACTIVE
from werkzeug.security import generate_password_hash


def setup_db():
    app = create_app()
    with app.test_request_context():
        db.init_app(app)
        db.drop_all()
        db.create_all()
        admin = User(
            username='admin',
            password=generate_password_hash('12345'),
            first_name='alex',
            last_name='fisher',
            email='fisherius@mail.ru',
            role=ADMIN,
            status=ACTIVE
        )
        db.session.add(admin)
        for i in range(1, 10):
            cat = Category(title=f'Category {i}', description='Auto create test category')
            db.session.add(cat)
        db.session.commit()


setup_db()


