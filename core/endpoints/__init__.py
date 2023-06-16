from .auth import bp as bp_auth
from .blog import bp as bp_blog
from .error import bp as bp_error

__all__ = (
    bp_auth,
    bp_blog,
    bp_error
)
