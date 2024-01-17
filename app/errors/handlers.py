from flask import render_template
from app.errors import bp

@bp.app_errorhandler
def not_found_error(error):
    return render_template('errors/404.jinja2'), 404

@bp.app_errorhandler
def internal_error(error):
    #current_appdb.session.rollback()
    return render_template('errors/404.jinja2'), 500
