from datetime import datetime

from core.db import db

mtm_in_favorite = db.Table(
    "favorite_blog",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("blog_id", db.Integer, db.ForeignKey("blog.id"), primary_key=True),
)

mtm_likes = db.Table(
    "blog_likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("blog_id", db.Integer, db.ForeignKey("blog.id"), primary_key=True),
)

mtm_dislikes = db.Table(
    "blog_dislikes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("blog_id", db.Integer, db.ForeignKey("blog.id"), primary_key=True),
)

mtm_tags = db.Table(
    "blog_tags",
    db.Column("blog_id", db.Integer, db.ForeignKey("blog.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(123), nullable=False)
    blog_text = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edit_date = db.Column(
        db.DateTime,
        # onupdate=datetime.now,
    )

    is_public = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)

    # set relation for author with User
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", backref=db.backref("blogs", lazy=True))
    # set relation for Blog with Category
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref=db.backref("blogs", lazy=True))
    # set relation for favorite blog with User
    in_favorite = db.relationship(
        "User",
        secondary=mtm_in_favorite,
        lazy="subquery",
        backref=db.backref("favorite_blogs", lazy=True),
    )
    # set relation for like with User
    likes = db.relationship(
        "User",
        secondary=mtm_likes,
        lazy="subquery",
        backref=db.backref("likes_blogs", lazy=True),
    )
    # set relation for dislike with User
    dislikes = db.relationship(
        "User",
        secondary=mtm_dislikes,
        lazy="subquery",
        backref=db.backref("dislikes_blogs", lazy=True),
    )

    def __repr__(self):
        return f"< Blog: {self.title} >"

    def avg_rating(self):
        if len(self.reviews) == 0:
            return None
        avg_rating = 0
        for r in self.reviews:
            avg_rating += r.rating
        return avg_rating / len(self.reviews)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))

    def __repr__(self):
        return f"< Category: {self.title} >"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)
    create_data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # set relation with Blog
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"), nullable=False)
    blog = db.relationship("Blog", backref=db.backref("reviews", lazy=True))
    # set relation for author with User
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", backref=db.backref("reviews", lazy=True))

    def __repr__(self):
        return f'< Review by {self.author.username} on blog #"{self.blog.id}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # set relation for author with User
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", backref=db.backref("comments", lazy=True))

    # set relation with Blog
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"), nullable=False)
    blog = db.relationship("Blog", backref=db.backref("comments", lazy=True))

    def __repr__(self):
        return f" Comment by {self.author.username} for blog #{self.blog.id}"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(24), nullable=False)
    # set relation with Blog
    blogs = db.relationship(
        "Blog",
        secondary=mtm_tags,
        lazy="subquery",
        backref=db.backref("tags", lazy=True),
    )
