import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Test(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))

    def __repr__(self):
        return '<Test {}>'.format(self.body)