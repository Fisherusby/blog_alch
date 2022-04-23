from flaskblog.db import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

# # many-to-many link table
# friend_mtm_hobby_table = Table(
#     'friend_mtm_hobby',
#     Base.metadata,
#     Column('friend_id', Integer, ForeignKey('friend.id')),
#     Column('hobby_id', Integer, ForeignKey('hobby.id'))
# )


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(123), nullable=False)
    blog_text = db.Column(db.Text, nullable=False)
    # User
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('blogs', lazy=True))
    # Category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('blogs', lazy=True))

    create_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    edit_date = db.Column(db.DateTime,
                          # onupdate=datetime.now,
                          )

    is_public = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'Blog: {self.title}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))

    def __repr__(self):
        return f'Category: {self.title}'




