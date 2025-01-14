from flask_login import UserMixin
from typing import Optional
import sqlalchemy as sa
from sqlalchemy import Enum
from app import db
from sqlalchemy import ForeignKey
import sqlalchemy.orm as so
import pytz, datetime, enum

moscow_tz = pytz.timezone('Europe/Moscow')

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    first_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), nullable=True)
    last_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), nullable=True)
    active_applications: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    level: so.Mapped[int] = so.mapped_column(sa.Integer)
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.id)
    

class ContractStatus(enum.Enum):
    active = "active"
    closed = "closed"
    checked = "checked"
    worked = "worked"


class Contract(db.Model):
    __tablename__ = 'contracts'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    created_at: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime(timezone=True), 
        nullable=False, 
        default=lambda: datetime.datetime.now(moscow_tz)
    )
    address: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    client: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    amount: so.Mapped[Optional[float]] = so.mapped_column(sa.Float, nullable=True)
    recommendations: so.Mapped[Optional[str]] = so.mapped_column(sa.Text, nullable=True)
    performer: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    acceptance_date: so.Mapped[Optional[sa.DateTime]] = so.mapped_column(sa.DateTime, nullable=True)

    photo_receipt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    photo_document_face: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    photo_document_back: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)

    scan_receipt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    scan_document_face: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    scan_document_back: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    
    # Добавляем колонку status с типом Enum
    status: so.Mapped[ContractStatus] = so.mapped_column(Enum(ContractStatus), nullable=False, default=ContractStatus.active)

    services: so.Mapped[list["Service"]] = so.relationship("Service", back_populates="contract")

    def __repr__(self):
        return f'<Contract {self.id}, {self.address}, Status {self.status}>'


class Service(db.Model):
    __tablename__ = 'services'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    contract_id: so.Mapped[int] = so.mapped_column(sa.Integer, ForeignKey('contracts.id'), nullable=False)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    price: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    sum: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)  # Сумма услуги
    warranty: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)

    # Используем relationship для обратной связи с договором
    contract: so.Mapped["Contract"] = so.relationship("Contract", back_populates="services")

    def __repr__(self):
        return f'<Service {self.name}, Contract ID {self.contract_id}>'

