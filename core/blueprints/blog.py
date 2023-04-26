from datetime import datetime

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, session, url_for)
from sqlalchemy.sql import desc, func, label, or_

from core.db import db
from core.forms import BlogForm, CommentForm, ReviewForm
from core import permissions
from core.models import Blog, Category, Comment, Review, User

bp = Blueprint("blog", __name__, url_prefix="/")


@bp.before_request
def category_load():
    cat_count = (
        db.session.query(Blog.category_id, func.count("*").label("blogs_count"))
        .group_by(Blog.category_id)
        .subquery()
    )
    cat3 = (
        db.session.query(Category, label("blogs_count", cat_count.c.blogs_count))
        .outerjoin(cat_count, Category.id == cat_count.c.category_id)
        .order_by(desc("blogs_count"))
        .all()
    )
    cat_list = []
    for cat, cat_count in cat3:
        cat.cat_count = cat_count
        cat_list.append(cat)
    g.category_list = cat_list


@bp.route("/")
def index():
    if "cat" in request.args:
        blogs = Blog.query.filter_by(
            category_id=request.args["cat"], is_public=True
        ).all()
    else:
        blogs = Blog.query.filter_by(is_public=True).all()
    return render_template("blog/blog_list.html", blogs_list=blogs)


@bp.route("/detail/<int:blog_id>", methods=["GET", "POST"])
def detail(blog_id):
    blog = (
        Blog.query.filter_by(id=blog_id)
        .filter(or_(Blog.is_public, Blog.author == g.user))
        .first()
    )

    if blog is None:
        abort(404)

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment()
        comment_form.populate_obj(comment)
        # Clear data because we will don't do redirect
        comment_form.text.data = ""
        comment.author_id = g.user.id
        comment.blog_id = blog_id
        db.session.add(comment)
        flash("Your comment add", "primary")

    if request.method == "GET":
        blog.view_count += 1
        db.session.add(blog)

    db.session.commit()
    return render_template(
        "blog/blog_detail.html", blog=blog, comment_form=comment_form
    )


@bp.route("/add", methods=["GET", "POST"])
@permissions.is_auth
def add():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog()
        form.populate_obj(blog)
        blog.author_id = g.user.id
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("blog.detail", blog_id=blog.id))
    return render_template("blog/form_blog.html", form=form)


@bp.route("/edit/<int:blog_id>", methods=["GET", "POST"])
@permissions.is_auth
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
        flash("Blog has been successfully edited.", "success")
        return redirect(url_for("blog.detail", blog_id=blog.id))

    return render_template("blog/form_blog.html", form=form)


@bp.route("/delete/<int:blog_id>")
@permissions.is_auth
def delete(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        if blog.author_id == g.user.id:
            db.session.delete(blog)
            db.session.commit()
            flash(f'Blog "{blog.title}" is delete!!!', "warning")
        else:
            flash(f"This blog do not your!!!", "danger")
            abort(403)
    else:
        abort(404)

    return redirect(url_for("blog.index"))


@bp.route("/my_blogs")
@permissions.is_auth
def my_blogs():
    blogs_list = Blog.query.filter_by(author_id=g.user.id)
    return render_template("blog/blog_list.html", blogs_list=blogs_list)


@bp.route("/favorite_blogs")
@permissions.is_auth
def favorite_blogs():
    blogs_list = (
        Blog.query.filter_by(is_public=True)
        .filter(Blog.in_favorite.any(id=g.user.id))
        .all()
    )
    return render_template("blog/blog_list.html", blogs_list=blogs_list)


@bp.route("/to_favorite/<int:blog_id>")
@permissions.is_auth
def to_favorite(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is not None:
        if g.user in blog.in_favorite:
            blog.in_favorite.remove(g.user)
            flash(f'Blog "{blog.title}" remove from favorite', "warning")
        else:
            blog.in_favorite.append(g.user)
            flash(f'Blog "{blog.title}" add to favorite', "primary")

        # fix increase views count after redirect
        blog.view_count -= 1

        db.session.commit()
    else:
        abort(404)
    return redirect(url_for("blog.detail", blog_id=blog_id))


@bp.route("/review/detail/<int:blog_id>")
def review_detail(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is None:
        abort(404)

    return blog_id


@bp.route("/review/add/<int:blog_id>", methods=["GET", "POST"])
@permissions.is_auth
def review_add(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is None:
        abort(404)

    review = Review.query.filter_by(blog_id=blog.id, author_id=g.user.id).first()
    if review is not None:
        flash("You can't add review because you already do it", "danger")
        return redirect(url_for("blog.detail", blog_id=blog.id))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review()
        form.populate_obj(review)
        review.blog_id = blog.id
        review.author_id = g.user.id
        db.session.add(review)
        db.session.commit()
        flash("Your comment add", "primary")
        return redirect(url_for("blog.review_detail", blog_id=blog.id))

    return render_template("blog/form_review.html", blog=blog, form=form)


@bp.route("/review/edit/<int:review_id>")
@permissions.is_auth
def review_edit(blog_id):
    pass


@bp.route("/comment/add/<int:blog_id>")
@permissions.is_auth
def comment_add(blog_id):
    pass


@bp.route("/comment/delete/<int:comment_id>")
@permissions.is_auth
def comment_delete(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if comment is None:
        flash(f"Comment #{comment_id} not found", "danger")
        abort(404)

    if comment.author != g.user:
        flash(f"This comment is not your", "danger")
        abort(404)

    db.session.delete(comment)
    db.session.commit()
    flash("Your comment has been removed", "warning")
    return redirect(url_for("blog.detail", blog_id=comment.blog_id))


@bp.route("/comment/edit/<int:comment_id>")
@permissions.is_auth
def comment_edit(comment_id):
    pass
