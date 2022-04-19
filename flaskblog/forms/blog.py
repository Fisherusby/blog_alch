from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class BlogForm(FlaskForm):
    title = StringField('Blog title', validators=[DataRequired()], render_kw={"placeholder": "Enter blog title"})
    blog_text = TextAreaField('Blog text', validators=[DataRequired()], render_kw={"placeholder": "Enter blog text"})
