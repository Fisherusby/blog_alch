from typing import List
from core import models, forms
from core.services.base import CRUDService
from sqlalchemy import select, func, label, desc
from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)


class BlogService(CRUDService):

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

    def create_blog(self):
        pass

    def get_blogs(self, category_id: int = None) -> List[models.Blog]:
        query = select(self.model).filter(self.model.is_public.is_(True))
        if category_id is not None:
            query = query.filter(self.model.category_id == category_id)
        return self.session.execute(query).scalars().all()


blog_service: BlogService = BlogService(models.Blog, forms.BlogForm)
