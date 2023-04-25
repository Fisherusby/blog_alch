from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import QuerySelectField

from core.models import Category


def get_category():
    return Category.query


class BlogForm(FlaskForm):
    category = QuerySelectField(
        "Category",
        get_label="title",
        allow_blank=True,
        validators=[DataRequired()],
        blank_text="Select a category",
        render_kw={"size": 1},
        query_factory=get_category,
        get_pk=lambda a: a.id,
    )

    title = StringField(
        "Blog title",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter blog title"},
    )
    blog_text = TextAreaField(
        "Blog text",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter blog text"},
    )
    is_public = BooleanField("Public")


class ReviewForm(FlaskForm):
    title = StringField(
        "title",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter title review for blog"},
    )
    text = TextAreaField(
        "text",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter review for blog"},
    )
    rating = SelectField(
        "rating",
        validators=[DataRequired()],
        choices=[
            ("", "Select a rating"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
        ],
        render_kw={"placeholder": "Enter review for blog"},
    )


class CommentForm(FlaskForm):
    text = TextAreaField(
        "Comment",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your comment"},
    )
