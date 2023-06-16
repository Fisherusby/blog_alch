from typing import Union
from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from core.db import db
from core.forms import LoginForm, RegistrationForm
from core import permissions, models, services

from werkzeug.wrappers import Response as BaseResponse

bp: Blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_user():
    g.user = None
    if "user_id" in session:
        g.user = services.user.get(id=session["user_id"])


@bp.route("/login", methods=["GET", "POST"])
@permissions.is_anonim
def login() -> Union[str, BaseResponse]:
    return services.user.authenticate()


@bp.route("/logout")
@permissions.is_auth
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/registration", methods=["GET", "POST"])
@permissions.is_anonim
def registration() -> Union[str, BaseResponse]:
    return services.user.registration()
