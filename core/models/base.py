from core.db import db
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import as_declarative


@as_declarative()
class AbstractBaseModel(db.Model):
    __abstract__ = True

    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())
