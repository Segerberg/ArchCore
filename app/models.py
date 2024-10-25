from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

# Association table for many-to-many relationship between nodes
node_association = sa.Table(
    'node_association',
    db.Model.metadata,
    sa.Column('parent_id', sa.Integer, sa.ForeignKey('nodes.id', ondelete='CASCADE'), primary_key=True),
    sa.Column('child_id', sa.Integer, sa.ForeignKey('nodes.id', ondelete='CASCADE'), primary_key=True),
    sa.Column('association_type', sa.String(50))
)

# Association table for the many-to-many relationship between Agent and Node
agent_node_association = sa.Table(
    'agent_node_association',
    db.Model.metadata,
    sa.Column('agent_id', sa.Integer, sa.ForeignKey('agents.id', ondelete='CASCADE'), primary_key=True),
    sa.Column('node_id', sa.Integer, sa.ForeignKey('nodes.id', ondelete='CASCADE'), primary_key=True),
    sa.Column('association_type', sa.String(50))
)

class Agent(db.Model):
    __tablename__ = 'agents'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(50))
    name: so.Mapped[str] = so.mapped_column(sa.String(50))
    description: so.Mapped[str] = so.mapped_column(sa.String(50))
    date_start: so.Mapped[datetime] = so.mapped_column(nullable=True)
    date_end: so.Mapped[datetime] = so.mapped_column(nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    # One-to-many relationship with Identifiers
    identifiers: so.Mapped[list['Identifier']] = so.relationship('Identifier', back_populates='agent')

    # Many-to-many relationship with Nodes
    nodes: so.Mapped[list['Node']] = so.relationship(
        'Node',
        secondary=agent_node_association,
        back_populates='agents'
    )

class Identifier(db.Model):
    __tablename__ = 'identifiers'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    identifier_type: so.Mapped[str] = so.mapped_column(sa.String(50))
    value: so.Mapped[str] = so.mapped_column(sa.String(100))
    agent_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('agents.id'))

    # Relationship back to Agent
    agent: so.Mapped['Agent'] = so.relationship('Agent', back_populates='identifiers')

class Node(db.Model):
    __tablename__ = 'nodes'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    ref_code: so.Mapped[str] = so.mapped_column(sa.String(50))
    level_of_description: so.Mapped[str] = so.mapped_column(sa.String(50))
    date_start: so.Mapped[datetime] = so.mapped_column(nullable=True)
    date_end: so.Mapped[datetime] = so.mapped_column(nullable=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(50))
    extent: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    archival_history: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    # Many-to-Many relationships
    related_nodes: so.Mapped[list['Node']] = so.relationship(
        'Node',
        secondary=node_association,
        primaryjoin=id == node_association.c.parent_id,
        secondaryjoin=id == node_association.c.child_id,
        backref=so.backref('related_nodes_backref', lazy='dynamic'),
        lazy='dynamic'
    )

    # Self-referential relationship: parent-child nodes
    parent_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey('nodes.id', ondelete='CASCADE'), nullable=True)
    parent: so.Mapped[Optional['Node']] = so.relationship(
        'Node', remote_side=[id], backref=so.backref('children', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    )

    # Many-to-many relationship with Agents
    agents: so.Mapped[list['Agent']] = so.relationship(
        'Agent',
        secondary=agent_node_association,
        back_populates='nodes'
    )

    __table_args__ = (
        sa.UniqueConstraint('ref_code', 'parent_id', name='uq_ref_code_parent_id'),
    )

    def is_top_node(self) -> bool:
        """Check if the node is the top node of the tree."""
        return self.parent is None

    def get_top_node(self) -> 'Node':
        """Retrieve the top node of the tree starting from any sub-node."""
        current_node = self
        while current_node.parent is not None:
            current_node = current_node.parent
        return current_node

    def get_all_parent_nodes(self) -> list:
        """Retrieve all parent nodes for the current node recursively."""
        parents = []
        current_node = self

        while current_node.parent is not None:
            parents.append(current_node.parent)
            current_node = current_node.parent

        return parents[::-1]

    def get_sibling_nodes(self) -> list:
        """Retrieve all sibling nodes for the current node."""
        if self.parent:
            return [child for child in self.parent.children if child.id != self.id]
        return []

    def get_full_tree(self) -> dict:
        """Retrieve the full tree rooted at the current node."""
        tree = {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'children': [child.get_full_tree() for child in self.children]
        }
        return tree

    def __repr__(self):
        return '<Node {}>'.format(self.title)

class FormatRegistry(db.Model):
    __tablename__ = 'format_registry'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    puid: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, name="puid")
    format_name: so.Mapped[str] = so.mapped_column(sa.String(256))
    format_version: so.Mapped[str] = so.mapped_column(sa.String(64))
    pronom_xml: so.Mapped[str] = so.mapped_column(sa.String(256))
    preservation: so.Mapped[bool] = so.mapped_column()
    allowed: so.Mapped[bool] = so.mapped_column()
    group: so.Mapped[str] = so.mapped_column(sa.String(256), default='undefined')
    action: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)

    def __repr__(self):
        return '<Node {}>'.format(self.name)



