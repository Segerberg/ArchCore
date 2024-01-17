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
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Association table for many-to-many relationship between nodes
node_association = sa.Table('node_association', db.Model.metadata,
    sa.Column('parent_id', sa.Integer, sa.ForeignKey('node.id')),
    sa.Column('child_id', sa.Integer, sa.ForeignKey('node.id'))
)

class Node(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    #DENTITY STATEMENT AREA
    ref_code: so.Mapped[str] = so.mapped_column(sa.String(50))
    level_of_description: so.Mapped[str] = so.mapped_column(sa.String(50))
    date_start: so.Mapped[datetime] = so.mapped_column(nullable=True)
    date_end: so.Mapped[datetime] = so.mapped_column(nullable=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50))
    extent_medium: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    # Context
    archival_history: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    source_of_acquisition: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    # Content and structure
    scope_and_content: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    appraisal_destruction_scheduling: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    accruals: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    system_of_arrangement: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    # Condition Access / Use Area
    conditions_governing_access: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    conditions_governing_reproduction: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    languages_of_material: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    scripts_of_material: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    physical_characteristics_and_technical_requirements: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    # Allied materials
    existence_location_of_originals: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    #related_descriptions: so.Mapped[str] = so.mapped_column(sa.String(50))
    publication_note: so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    # Notes Area????
    # Access points
    #Description control Area
    status:so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    level_of_detail:so.Mapped[str] = so.mapped_column(sa.String(50),nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    sources: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)

    # Many-to-Many relationships
    related_nodes: so.Mapped[int] = so.relationship(
        'Node',
        secondary=node_association,
        primaryjoin=id == node_association.c.parent_id,
        secondaryjoin=id == node_association.c.child_id,
        backref=so.backref('related_nodes_backref', lazy='dynamic'),
        lazy='dynamic'
    )

    # Self-referential relationship: parent-child nodes
    parent_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('node.id'),nullable=True)
    parent: so.Mapped['Node'] = so.relationship(
        'Node', remote_side=[id], backref=so.backref('children', lazy='dynamic', primaryjoin='Node.id == Node.parent_id'))

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
            return [child for child in self.parent.children]
        return []

    def get_full_tree(self) -> dict:
        """Retrieve the full tree rooted at the current node."""
        tree = {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'children': [child.get_full_tree() for child in self.children]
        }
        return tree

    def __repr__(self):
        return '<Node {}>'.format(self.name)

