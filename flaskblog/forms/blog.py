from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms_alchemy import QuerySelectField
from wtforms.validators import DataRequired, Length
from flaskblog.models import Category


def get_category():
    return Category.query


class BlogForm(FlaskForm):
    category = QuerySelectField('Category',
        get_label='title',
        allow_blank=True,
        validators=[DataRequired()],
        blank_text='Select a category',
        render_kw={'size': 1},
        query_factory=get_category,
        get_pk=lambda a: a.id,
        )

    title = StringField('Blog title', validators=[DataRequired()], render_kw={"placeholder": "Enter blog title"})
    blog_text = TextAreaField('Blog text', validators=[DataRequired()], render_kw={"placeholder": "Enter blog text"})
    is_public = BooleanField('Public')
