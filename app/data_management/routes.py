import os

from flask import render_template, request, url_for, redirect, jsonify
from flask_login import login_required
from app.data_management import bp
from app.models import Node
from app import db
import sqlalchemy as sa
from sqlalchemy import func
from datetime import datetime
import uuid

@bp.route('/data-management', methods=['GET', 'POST'])
@login_required
def index():
    resources_count_query = sa.select(func.count()).where(Node.parent == None)
    resources_count_result = db.session.execute(resources_count_query)
    resources_count = resources_count_result.scalar()  # Get the scalar result (the count)

    return render_template('data_management/index.jinja2', resources_count=resources_count)


@bp.route('/data-management/authority_records', methods=['GET', 'POST'])
@login_required
def authority_records():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Node).where(Node.parent == None)
    #nodes = db.paginate(query,page=page, per_page=3, error_out=False)
    #next_url = url_for('data_management.archival_descriptions', page=nodes.next_num) \
    #    if nodes.has_next else None
    #prev_url = url_for('data_management.archival_descriptions', page=nodes.prev_num) \
    #    if nodes.has_prev else None

    return render_template('data_management/authority_records/index.jinja2')
                           #nodes=nodes,
                           #next_url=next_url,
                           #prev_url=prev_url)

@bp.route('/data-management/archival-descriptions', methods=['GET', 'POST'])
@login_required
def archival_descriptions():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Node).where(Node.parent == None)
    nodes = db.paginate(query,page=page, per_page=15, error_out=False)
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
def archival_descriptions_detail(id, reload=False):
    node = Node.query.get_or_404(id)
    first_level_children = node.children.all()  # Preload first-level children
    #if request.method == "POST":
    #    return render_template('data_management/archival_descriptions/node_detail.jinja2', node=node)

    #return render_template('data_management/archival_descriptions/node.jinja2', node=node, reload=reload)
    return render_template('data_management/archival_descriptions/tree.jinja2', node=node, reload=reload)



@bp.route('/node/<int:node_id>/children', methods=['GET'])
def get_children(node_id):
    node = Node.query.get_or_404(node_id)
    children = node.children.all()
    return render_template('data_management/archival_descriptions/_children.jinja2', children=children)


@bp.route('/node/<int:node_id>/details', methods=['GET'])
def get_node_details(node_id):
    node = Node.query.get_or_404(node_id)
    return render_template('data_management/archival_descriptions/node_detail.jinja2', node=node)


@bp.route('/data-management/archival-descriptions/node/<id>', methods=['GET', 'POST'])
@login_required
def get_node(id):
    full_tree = request.args.get('full_tree')
    node = Node.query.get(id)
    if full_tree and not node.is_top_node():
        node = node.query.get(node.get_top_node().id)

    return render_template('data_management/archival_descriptions/_tree_node.jinja2', node=node)


@bp.route('/node/<int:node_id>/edit', methods=['GET', 'POST'])
def edit_node(node_id):
    node = Node.query.get_or_404(node_id)
    lod_list = os.getenv('LEVELS_OF_DESCRIPTION').split(',')

    if request.method == 'POST':
        node.title = request.form['title']
        if request.form['date_start']:
            node.date_start = datetime.strptime(request.form['date_start'], "%Y-%m-%d").date()
        if request.form['date_end']:
            node.date_end = datetime.strptime(request.form['date_end'], "%Y-%m-%d").date()
        node.archival_history = request.form['archival_history']
        node.level_of_description = request.form['level_of_description']

        db.session.commit()

        # Return the updated node details after saving
        return render_template('data_management/archival_descriptions/node_detail.jinja2', node=node)

    # Render the edit form
    return render_template('data_management/archival_descriptions/_edit_node.jinja2', node=node, lod_list=lod_list)


@bp.route('/node/<int:parent_id>/add_child', methods=['GET', 'POST'])
@bp.route('/node/add_root', methods=['GET', 'POST'])
@login_required
def add_node(parent_id=None):
    lod_list = os.getenv('LEVELS_OF_DESCRIPTION', '').split(',')
    parent_node = Node.query.get(parent_id) if parent_id else None

    if request.method == 'POST':
        node = Node(ref_code=str(uuid.uuid4()), level_of_description="box")
        node.title = request.form['title']

        if request.form.get('date_start'):
            date_start = datetime.strptime(request.form['date_start'], "%Y-%m-%d").date()
            node.date_start = date_start
        if request.form.get('date_end'):
            date_end = datetime.strptime(request.form['date_end'], "%Y-%m-%d").date()
            node.date_end = date_end
        node.archival_history = request.form.get('archival_history', '')
        node.level_of_description = request.form.get('level_of_description', 'box')
        node.parent = parent_node
        db.session.add(node)
        db.session.commit()
        if parent_node:
            return render_template('data_management/archival_descriptions/node_detail.jinja2', node=node)
        else:
            response = jsonify(success=True)  # Placeholder response
            response.headers['HX-Redirect'] = url_for('data_management.archival_descriptions_detail', id=node.id)
            return response
    else:
        if parent_node:
            return render_template('data_management/archival_descriptions/_add_node.jinja2', node=parent_node, parent_node=parent_node, lod_list=lod_list)
        else:
            return render_template('data_management/archival_descriptions/_add_root_node.jinja2', lod_list=lod_list)



@bp.route('/data-management/archival-descriptions/node/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_node(id):
    if request.method == 'POST':
        node = Node.query.get(id)
        top_node = node.get_top_node()
        if top_node == id:
            print("hek")
        db.session.delete(node)
        db.session.commit()

        return render_template('data_management/archival_descriptions/node.jinja2', node=top_node)

