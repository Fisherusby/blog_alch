from typing import List, Any, Optional
from core import models, forms
from core.services.base import BaseService
from sqlalchemy import select, func, label, desc, or_
from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)


class BlogService(BaseService):

    def get_categories_for_menu(self):
        query_count = select(models.Blog.category_id, func.count(models.Blog.id).label("blogs_count")) \
            .group_by(models.Blog.category_id) \
            .subquery('t_count')
        query = select(models.Category, label("blogs_count", query_count.c.blogs_count)) \
            .outerjoin(query_count, models.Category.id == query_count.c.category_id) \
            .order_by(desc("blogs_count"))

        result: List[models.Category, int] = self.session.execute(query).all()
        categories: list = []
        for category, blog_count in result:
            category.blog_count = blog_count
            categories.append(category)
        g.category_list = categories

    def form_blog(self, blog_id: Any = None):
        if blog_id is not None:
            form, blog = self.form_submit(obj_id=blog_id)
        else:
            form, blog = self.form_submit(author_id=g.user.id)

        if blog is not None:
            return redirect(url_for("blog.detail", blog_id=blog.id))
        return render_template("blog/form_blog.html", form=form)

    def get_blog(self, blog_id: Any, not_exist_raise: bool = False) -> Optional[models.Blog]:
        query = select(models.Blog).filter(models.Blog.id == blog_id)\
            .filter(or_(models.Blog.is_public, models.Blog.author == g.user))

        blog: models.Blog = self.session.execute(query).scalar_one_or_none()

        if not_exist_raise and blog is None:
            abort(404)

        return blog

    def get_blogs(self, category_id: int = None) -> List[models.Blog]:
        query = select(self.model).filter(self.model.is_public.is_(True))
        if category_id is not None:
            query = query.filter(self.model.category_id == category_id)
        return self.session.execute(query).scalars().all()


blog_service: BlogService = BlogService(models.Blog, forms.BlogForm)
comment_service: BaseService = BaseService(models.Comment, forms.CommentForm)
