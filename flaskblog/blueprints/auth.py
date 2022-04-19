from flask import Blueprint, request, redirect, render_template, url_for, abort, flash, session
from flaskblog.db import db
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog.models import User
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None:
            if check_password_hash(user.password, request.form['password']):
                session['username'] = user.username
                session['last_name'] = user.last_name
                session['first_name'] = user.first_name
                session['user_id'] = user.id
                session['login'] = True
                flash(f'Hello, {user.username}', "primary")
                return redirect(url_for('blog.index'))

        flash(f'User or password not found', "danger")

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=request.form['username'],
            password=generate_password_hash(request.form['password']),
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/form_register.html', form=form)

