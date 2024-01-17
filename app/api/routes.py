from app.api import bp

@bp.route('/api', methods=['GET', 'POST'])
def api():
    return 200
