from core.db import db

# User role
USER = 0
STAFF = 1
ADMIN = 2

ROLE = {
    ADMIN: "admin",
    STAFF: "staff",
    USER: "user",
}

# user status
INACTIVE = 0
NEW = 1
ACTIVE = 2

STATUS = {
    INACTIVE: "inactive",
    NEW: "new",
    ACTIVE: "active",
}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    status = db.Column(db.SmallInteger, default=NEW)
    role = db.Column(db.SmallInteger, default=USER)

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_status(self):
        return STATUS[self.status]

    def get_role(self):
        return ROLE[self.role]
