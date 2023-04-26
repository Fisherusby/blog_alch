from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from core.db import db
from core.forms import LoginForm, RegistrationForm
from core import permissions
from core.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_user():
    g.user = None
    if "user_id" in session:
        g.user = User.query.filter_by(id=session["user_id"]).first()


@bp.route("/login", methods=["GET", "POST"])
@permissions.is_anonim
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=request.form["username"]).first()
        if user is not None:
            if check_password_hash(user.password, request.form["password"]):
                session["user_id"] = user.id
                session["login"] = True
                flash(f"Hello, {user.username}", "primary")
                if "next" in request.args:
                    return redirect(request.args["next"])
                return redirect(url_for("blog.index"))

        flash(f"User or password not found", "danger")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@permissions.is_auth
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/registration", methods=["GET", "POST"])
@permissions.is_anonim
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
        flash(f"User {user.username} created! You can login now!", "primary")
        return redirect(url_for("auth.login"))
    return render_template("auth/form_register.html", form=form)
