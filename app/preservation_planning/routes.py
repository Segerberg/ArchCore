
from flask import render_template
from flask_login import login_required
from app.preservation_planning import bp

@bp.route('/preservation-planning', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('preservation_planning/index.jinja2')
