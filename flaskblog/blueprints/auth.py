from flask import Blueprint, request, redirect, render_template, url_for, abort, flash, session, g
from flaskblog.db import db
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog.login import is_anonim
from flaskblog.models import User
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_user():
    g.user = None
    if "user_id" in session:
        g.user = User.query.filter_by(id=session["user_id"]).first()


@bp.route('/login', methods=["GET", "POST"])
@is_anonim
def login():
    form = LoginForm()
    print(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=request.form['username']).first()
        print(user)
        if user is not None:
            if check_password_hash(user.password, request.form['password']):
                session['user_id'] = user.id
                session['login'] = True
                flash(f'Hello, {user.username}', "primary")
                if 'next' in request.args:
                    return redirect(request.args['next'])
                return redirect(url_for('blog.index'))

        flash(f'User or password not found', "danger")

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/registration', methods=['GET', 'POST'])
@is_anonim
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            # username=request.form['username'],
            #
            # first_name=request.form['first_name'],
            # last_name=request.form['last_name'],
            # email=request.form['email'],
        )
        form.populate_obj(user)
        user.password = generate_password_hash(user.password)
        db.session.add(user)
        db.session.commit()
        flash(f'User {user.username} created! You can login now!', 'primary')
        return redirect(url_for('auth.login'))
    return render_template('auth/form_register.html', form=form)

