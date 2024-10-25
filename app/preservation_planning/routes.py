from flask import render_template, request, url_for
from flask_login import login_required
from app.preservation_planning import bp
import sqlalchemy as sa
from app import db
from app.models import FormatRegistry

@bp.route('/preservation-planning', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('preservation_planning/index.jinja2')

@bp.route('/preservation-planning/format-registry', methods=['GET', 'POST'])
@login_required
def format_registry():
    page = request.args.get('page', 1, type=int)
    query = sa.select(FormatRegistry)
    items = db.paginate(query,page=page, per_page=15, error_out=False)
    next_url = url_for('preservation_planning.format_registry', page=items.next_num) \
        if items.has_next else None
    prev_url = url_for('preservation_planning.format_registry', page=items.prev_num) \
        if items.has_prev else None

    return render_template('preservation_planning/format_registry/index.jinja2',
                           items=items,
                           next_url=next_url,
                           prev_url=prev_url)
