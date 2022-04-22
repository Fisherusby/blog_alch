from flask import Blueprint, render_template, url_for, flash, redirect, request

bp = Blueprint('error', __name__)


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('_404.html'), 404


@bp.app_errorhandler(401)
def page_not_found(e):
    flash('You need to log in!', 'danger')
    return redirect(url_for('auth.login', next=request.url))


@bp.app_errorhandler(403)
def page_not_found(e):
    flash("Forbidden! You don't have the permission to access the requested resource.", 'danger')
    return redirect(url_for('blog.index'))

