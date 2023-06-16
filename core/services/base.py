from typing import List, TypeVar, Type, Any, Optional
from core.db import db
from sqlalchemy import select
from core.models.base import AbstractBaseModel
from flask_wtf import FlaskForm

from flask import (abort, flash, g,)

ModelType = TypeVar("ModelType", bound=AbstractBaseModel)
FormType = TypeVar("FormType", bound=FlaskForm)


class BaseService:

    def __init__(self, model: Type[ModelType], form: Type[FormType]):
        self.model = model
        self.form = form
        self.session = db.session

    def create(self, data: dict):

        return

    def create_multi(self, data: List[dict]):
        pass

    def get(self, id: Any) -> Optional[ModelType]:
        return self.session.execute(select(self.model).filter(self.model.id == id)).scalar_one_or_none()

    def get_multi(self, skip: int = 0, limit: int = 100, order: List[str] = None):
        query = select(self.model).offset(skip).limit(limit)
        if order is not None:
            query = query.order_by(*order)
        return self.session.execute(query).scalars().all()

    def get_by_field(self, field: str, value: str, only_one: bool = True):
        query = select(self.model).filter(getattr(self.model, field, None) == value)
        if only_one:
            return self.session.execute(query).scalar_one_or_none()
        else:
            return self.session.execute(query).scalars().all()

    def update(self):
        pass

    def update_multi(self):
        pass

    def delete(self):
        pass

    def add_obj(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def delete_obj(self, obj):
        self.session.delete(obj)
        self.session.commit()

    def form_submit(
            self, obj_id: Any = None, **kwargs
    ) -> (Type[FormType], Optional[Type[ModelType]]):
        obj = self.get_or_404(obj_id=obj_id)

        if obj is not None:
            self.is_owner(obj=obj, user=g.user)

        form: Type[FormType] = self.form(obj=obj)
        if form.validate_on_submit():
            if obj is None:
                obj: Type[ModelType] = self.model()
            form.populate_obj(obj)
            for attr, value in kwargs.items():
                obj.__setattr__(attr, value)
            obj = self.add_obj(obj)
            return form, obj
        return form, None

    def delete_by_owner(self, obj_id: Any):
        obj: Type[ModelType] = self.get_or_404(obj_id=obj_id)
        self.is_owner(obj=obj, user=g.user)
        self.delete_obj(obj)

    def get_or_404(self, obj_id: Any) -> Optional[Type[ModelType]]:
        obj: Type[ModelType] = self.get(id=obj_id)
        if obj is None and obj_id is not None:
            # flash(f"Unable to edit #{obj_id}", "danger")
            abort(404)
        return obj

    def is_owner(self, obj: Type[ModelType], user: Any, raise_not_owner: bool = True):
        if obj.owner_id is None:
            return False

        if user is not None and obj.owner_id == user.id:
            return True

        if raise_not_owner:
            # flash(f"Access to edit #{obj.id} deny", "danger")
            abort(403)
        return False
