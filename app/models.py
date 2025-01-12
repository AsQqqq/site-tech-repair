from flask_login import UserMixin
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    first_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), nullable=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    level: so.Mapped[int] = so.mapped_column(sa.Integer)  # Пример использования Integer для поля level
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.id)
