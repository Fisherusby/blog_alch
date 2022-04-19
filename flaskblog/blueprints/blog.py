from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, session
from flaskblog.db import db
from flaskblog.models import User, Blog
from flaskblog.forms import BlogForm

bp = Blueprint('blog', __name__, url_prefix='/')


@bp.route('/')
def index():
    blogs = Blog.query.all()
    print(blogs)
    return render_template('blog/blog_list.html', blogs_list=blogs)


@bp.route('/detail/<int:blog_id>')
def detail(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    print(blog)
    if blog is not None:
        return render_template('blog/blog_detail.html', blog=blog)
    else:
        abort(404)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(
            title=request.form['title'],
            blog_text=request.form['blog_text'],
            author_id=session['user_id'],
        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blog.detail', blog_id=blog.id))
    return render_template('blog/form_blog.html', form=form)


@bp.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit(blog_id):

    blog = Blog.query.filter_by(id=blog_id).first()

    if blog is None:
        flash(f"Unable to edit blog #{blog_id}", "danger")
        abort(404)

    if blog.author_id != session['user_id']:
        flash(f"Access to edit blog #{blog_id} deny", "danger")
        abort(404)

    form = BlogForm(data=blog.__dict__)

    if form.validate_on_submit():
        blog.title = request.form['title']
        blog.blog_text = request.form['blog_text']
        db.session.add(blog)
        db.session.commit()
        flash('Blog has been successfully edited.', 'success')
        return redirect(url_for('blog.detail', blog_id=blog.id))

    return render_template('blog/form_blog.html', form=form)


@bp.route('/delete/<int:blog_id>')
def delete(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        if blog.author_id == session.get('user_id'):
            db.session.delete(blog)
            db.session.commit()
            flash(f'Blog "{blog.title}" is delete!!!', "warning")
        else:
            flash(f'This blog do not your!!!', "danger")
    else:
        abort(404)

    return redirect(url_for('blog.index'))


@bp.route('/my_blogs')
def my_blogs():
    blogs_list = Blog.query.filter_by(author_id=session['user_id'])
    return render_template('blog/blog_list.html', blogs_list=blogs_list)

