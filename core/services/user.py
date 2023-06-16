from core import models, forms
from core.services.base import BaseService

from flask import (abort, flash, g, request, redirect, url_for, render_template, session)

from werkzeug.security import check_password_hash, generate_password_hash


class UserService(BaseService):
    def registration(self):
        attr = {}
        if request.form.get('password') is not None:
            attr['password'] = generate_password_hash(request.form['password'])

        form, user = self.form_submit(**attr)
        if user is not None:
            return redirect(url_for("auth.login"))
        return render_template("auth/form_register.html", form=form)

    def authenticate(self):
        form: forms.LoginForm = forms.LoginForm()
        if form.validate_on_submit():
            user: models.User = self.get_by_field(field='username', value=request.form["username"])
            if user is not None and check_password_hash(user.password, request.form["password"]):
                session["user_id"]: int = user.id
                session["login"]: bool = True
                flash(f"Hello, {user.username}", "primary")
                if "next" in request.args:
                    return redirect(request.args["next"])
                return redirect(url_for("blog.index"))

            flash(f"User or password not found", "danger")

        return render_template("auth/login.html", form=form)


user_service: UserService = UserService(model=models.User, form=forms.RegistrationForm)
