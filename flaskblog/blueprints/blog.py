from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, session, g
from flaskblog.db import db
from flaskblog.models import User, Blog, Category
from flaskblog.forms import BlogForm
from flaskblog.login import is_auth, is_anonim, is_admin
from sqlalchemy.sql import func, desc, label
from datetime import datetime

bp = Blueprint('blog', __name__, url_prefix='/')


@bp.before_request
def category_load():
    cat_count = db.session.query(Blog.category_id, func.count('*').label('blogs_count')).\
        group_by(Blog.category_id).subquery()
    cat3 = db.session.query(Category, label('blogs_count', cat_count.c.blogs_count)).\
        outerjoin(cat_count, Category.id == cat_count.c.category_id).order_by(desc('blogs_count')).all()
    cat_list = []
    for cat, cat_count in cat3:
        cat.cat_count = cat_count
        cat_list.append(cat)
    g.categorys = cat_list


@bp.route('/')
def index():
    if 'cat' in request.args:
        blogs = Blog.query.filter_by(category_id=request.args['cat'], is_public=True).all()
    else:
        blogs = Blog.query.filter_by(is_public=True).all()
    return render_template('blog/blog_list.html', blogs_list=blogs)


@bp.route('/detail/<int:blog_id>')
def detail(blog_id):
    blog = Blog.query.filter_by(id=blog_id, is_public=True).first()
    if blog is not None:
        blog.view_count += 1
        db.session.add(blog)
        db.session.commit()
        return render_template('blog/blog_detail.html', blog=blog)
    else:
        abort(404)


@bp.route('/add', methods=['GET', 'POST'])
@is_auth
def add():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog()
        form.populate_obj(blog)
        blog.author_id = g.user.id
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blog.detail', blog_id=blog.id))
    return render_template('blog/form_blog.html', form=form)


@bp.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
@is_auth
def edit(blog_id):
    blog = Blog.query.get(blog_id)

    if blog is None:
        flash(f"Unable to edit blog #{blog_id}", "danger")
        abort(404)

    if blog.author_id != g.user.id:
        flash(f"Access to edit blog #{blog_id} deny", "danger")
        abort(403)

    form = BlogForm(obj=blog)

    if form.validate_on_submit():
        form.populate_obj(blog)
        blog.edit_date = datetime.now()
        db.session.add(blog)
        db.session.commit()
        flash('Blog has been successfully edited.', 'success')
        return redirect(url_for('blog.detail', blog_id=blog.id))

    return render_template('blog/form_blog.html', form=form)


@bp.route('/delete/<int:blog_id>')
@is_auth
def delete(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        if blog.author_id == g.user.id:
            db.session.delete(blog)
            db.session.commit()
            flash(f'Blog "{blog.title}" is delete!!!', "warning")
        else:
            flash(f'This blog do not your!!!', "danger")
            abort(403)
    else:
        abort(404)

    return redirect(url_for('blog.index'))


@bp.route('/my_blogs')
@is_auth
def my_blogs():
    blogs_list = Blog.query.filter_by(author_id=g.user.id)
    return render_template('blog/blog_list.html', blogs_list=blogs_list)

