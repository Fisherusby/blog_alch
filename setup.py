from flaskblog.db import db
from flaskblog import create_app
from flaskblog.models import Category, User
from flaskblog.models.user import ADMIN, ACTIVE
from werkzeug.security import generate_password_hash
import re
from getpass import getpass


def gen_admin():
    username = input('Enter user name: ')
    while True:
        password = getpass('Enter password: ')
        confirm_password = getpass('Confirm password: ')
        if password == confirm_password:
            break
        else:
            print('Passwords not match. Need try again!')

    while True:
        email = input('Enter email: ')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print(f'Email "{email}" is not valid. Need try again!')
        else:
            break

    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')

    return User(
        username=username,
        password=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=ADMIN,
        status=ACTIVE
    )


def setup_db():
    app = create_app()
    with app.test_request_context():
        db.init_app(app)
        print('Delete all tables')
        db.drop_all()
        print('Create all tables')
        db.create_all()
        print('Create admin')

        admin = gen_admin()

        db.session.add(admin)
        print('Create categories:')
        for i in range(1, 10):
            cat = Category(title=f'Category {i}', description='Auto create test category')
            print(f'   add {cat.title}')
            db.session.add(cat)
        db.session.commit()


setup_db()


