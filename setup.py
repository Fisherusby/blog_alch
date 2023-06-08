import re
from getpass import getpass

from werkzeug.security import generate_password_hash

from core import create_app
from core.db import db
from core.models import Category, User

default_username = 'User'
default_password = 'user'
default_email = 'user@example.com'
default_first_name = 'User'
default_last_name = 'User'


def gen_admin():
    username = input(f"Enter user name (default={default_username}): ") or default_username
    while True:
        password = getpass(f"Enter password (default={default_password}): ") or default_password
        confirm_password = getpass(f"Confirm password (default={default_password}): ") or default_password
        if password == confirm_password:
            break
        else:
            print("Passwords not match. Need try again!")

    while True:
        email = input(f"Enter email (default={default_email}): ") or default_email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print(f'Email "{email}" is not valid. Need try again!')
        else:
            break

    first_name = input(f"Enter first name (default={default_first_name}): ") or default_first_name
    last_name = input(f"Enter last name (default={default_last_name}): ") or default_last_name

    return User(
        username=username,
        password=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=User.ADMIN,
        status=User.ACTIVE,
    )


def setup_db():
    app = create_app()
    with app.test_request_context():
        print("Delete all tables")
        db.drop_all()
        print("Create all tables")
        db.create_all()
        print("Create admin")

        admin = gen_admin()

        db.session.add(admin)
        print("Create categories:")
        for i in range(1, 10):
            cat = Category(
                title=f"Category {i}", description="Auto create test category"
            )
            print(f"   add {cat.title}")
            db.session.add(cat)
        db.session.commit()


if __name__ == '__main__':
    setup_db()
