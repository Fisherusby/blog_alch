from typing import List, Union

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)
from sqlalchemy.sql import or_

from werkzeug.wrappers import Response as BaseResponse

from core.db import db
from core import permissions, models, forms, services

bp: Blueprint = Blueprint("blog", __name__, url_prefix="/")


@bp.before_request
def category_load() -> None:
    services.blog.get_categories_for_menu()


@bp.route("/")
def index() -> str:
    category_id = request.args.get("cat")
    blogs: List[models.Blog] = services.blog.get_blogs(category_id=category_id)
    return render_template("blog/blog_list.html", blogs_list=blogs)


@bp.route("/detail/<int:blog_id>", methods=["GET", "POST"])
def detail(blog_id) -> str:
    blog: models.Blog = (
        models.Blog.query.filter_by(id=blog_id)
        .filter(or_(models.Blog.is_public, models.Blog.author == g.user))
        .first()
    )

    if blog is None:
        abort(404)

    comment_form: forms.CommentForm = forms.CommentForm()
    if comment_form.validate_on_submit():
        comment: models.Comment = models.Comment()
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
def add() -> Union[str, BaseResponse]:
    form, blog = services.blog.form_submit(author_id=g.user.id)
    if blog is not None:
        return redirect(url_for("blog.detail", blog_id=blog.id))

    return render_template("blog/form_blog.html", form=form)


@bp.route("/edit/<int:blog_id>", methods=["GET", "POST"])
@permissions.is_auth
def edit(blog_id: int) -> Union[str, BaseResponse]:
    form, blog = services.blog.form_submit(obj_id=blog_id, is_owner=True)
    if blog is not None:
        return redirect(url_for("blog.detail", blog_id=blog.id))

    return render_template("blog/form_blog.html", form=form)


@bp.route("/delete/<int:blog_id>")
@permissions.is_auth
def delete(blog_id: int) -> BaseResponse:
    blog: models.Blog = services.blog.get(id=blog_id)

    if blog is None:
        abort(404)

    if blog.author_id != g.user.id:
        flash(f"This blog do not your!!!", "danger")
        abort(403)

    db.session.delete(blog)
    db.session.commit()
    flash(f'Blog "{blog.title}" is delete!!!', "warning")

    return redirect(url_for("blog.index"))


@bp.route("/my_blogs")
@permissions.is_auth
def my_blogs() -> str:
    blogs_list: List[models.Blog] = models.Blog.query.filter_by(author_id=g.user.id)
    return render_template("blog/blog_list.html", blogs_list=blogs_list)


@bp.route("/favorite_blogs")
@permissions.is_auth
def favorite_blogs() -> str:
    blogs_list: List[models.Blog] = (
        models.Blog.query.filter_by(is_public=True)
        .filter(models.Blog.in_favorite.any(id=g.user.id))
        .all()
    )
    return render_template("blog/blog_list.html", blogs_list=blogs_list)


@bp.route("/to_favorite/<int:blog_id>")
@permissions.is_auth
def to_favorite(blog_id: int) -> BaseResponse:
    blog: models.Blog = services.blog.get(id=blog_id)

    if blog is None:
        abort(404)

    if g.user in blog.in_favorite:
        blog.in_favorite.remove(g.user)
        flash(f'Blog "{blog.title}" remove from favorite', "warning")
    else:
        blog.in_favorite.append(g.user)
        flash(f'Blog "{blog.title}" add to favorite', "primary")

    # fix increase views count after redirect
    blog.view_count -= 1

    db.session.commit()

    return redirect(url_for("blog.detail", blog_id=blog_id))


@bp.route("/review/detail/<int:blog_id>")
def review_detail(blog_id: int) -> int:
    blog: models.Blog = models.Blog.query.filter_by(id=blog_id).first()
    if blog is None:
        abort(404)

    return blog_id


@bp.route("/review/add/<int:blog_id>", methods=["GET", "POST"])
@permissions.is_auth
def review_add(blog_id: int) -> Union[str, BaseResponse]:
    blog: models.Blog = services.blog.get(id=blog_id)
    if blog is None:
        abort(404)

    review: models.Review = models.Review.query.filter_by(blog_id=blog.id, author_id=g.user.id).first()
    if review is not None:
        flash("You can't add review because you already do it", "danger")
        return redirect(url_for("blog.detail", blog_id=blog.id))

    form: forms.ReviewForm = forms.ReviewForm()
    if form.validate_on_submit():
        review = models.Review()
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
def review_edit(blog_id: id):
    pass


@bp.route("/comment/add/<int:blog_id>")
@permissions.is_auth
def comment_add(blog_id: id):
    pass


@bp.route("/comment/delete/<int:comment_id>")
@permissions.is_auth
def comment_delete(comment_id: id) -> BaseResponse:
    comment: models.Comment = models.Comment.query.filter_by(id=comment_id).first()

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
def comment_edit(comment_id: int):
    pass
