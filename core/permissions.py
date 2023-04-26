from functools import wraps

from flask import abort, flash, g, session


def login():
    pass


def is_auth(view):
    @wraps(view)
    def wrap_fun(**kwargs):
        if g.user is None:
            abort(401)
        return view(**kwargs)

    return wrap_fun


def is_admin(view):
    @wraps(view)
    def wrap_fun(**kwargs):
        if (
            session.get("login", False) is False
            or session.get("is_admin", False) is False
        ):
            abort(403)
        return view(**kwargs)

    return wrap_fun


def is_anonim(view):
    @wraps(view)
    def wrap_fun(**kwargs):
        if g.user is not None:
            abort(403)
        return view(**kwargs)

    return wrap_fun
