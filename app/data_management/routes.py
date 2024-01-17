
from flask import render_template, request, url_for
from flask_login import login_required
from app.data_management import bp
from app.models import Node
from app import db
import sqlalchemy as sa

@bp.route('/data-management', methods=['GET', 'POST'])
@login_required
def index():

    return render_template('data_management/index.jinja2')


@bp.route('/data-management/archival-descriptions', methods=['GET', 'POST'])
@login_required
def archival_descriptions():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Node).where(Node.parent == None)
    nodes = db.paginate(query,page=page, per_page=3, error_out=False)
    next_url = url_for('data_management.archival_descriptions', page=nodes.next_num) \
        if nodes.has_next else None
    prev_url = url_for('data_management.archival_descriptions', page=nodes.prev_num) \
        if nodes.has_prev else None

    return render_template('data_management/archival_descriptions/index.jinja2',
                           nodes=nodes,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/data-management/archival-descriptions/<id>', methods=['GET', 'POST'])
@login_required
def archival_descriptions_detail(id):
    node = Node.query.get(id)

    return render_template('data_management/archival_descriptions/node.jinja2', node=node)

@bp.route('/data-management/archival-descriptions/node/<id>', methods=['GET', 'POST'])
@login_required
def get_node(id):
    full_tree = request.args.get('full_tree')
    node = Node.query.get(id)
    if full_tree and not node.is_top_node():
        print('HEJ')
        node = node.query.get(node.get_top_node().id)
        print(node.name)


    return render_template('data_management/archival_descriptions/_tree_node.jinja2', node=node)


