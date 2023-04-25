from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from core.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter username"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", "Passwords must match"),
        ],
        render_kw={"placeholder": "Enter your password"},
    )

    confirm_password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Confirm your password"},
    )

    first_name = StringField(
        "First name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your first name"},
    )
    last_name = StringField(
        "Last name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your last name"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email"},
    )

    # submit = SubmitField('Registrate')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError("Username already used!")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError("User with this email already register!")
