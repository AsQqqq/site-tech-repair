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
    
    # Добавляем метод serialize
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'active_applications': self.active_applications,
            'level': self.level,
            'is_active': self.is_active
        }

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
    
    # Добавляем метод serialize
    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'address': self.address,
            'client': self.client,
            'description': self.description,
            'amount': self.amount,
            'recommendations': self.recommendations,
            'performer': self.performer,
            'number': self.number,
            'acceptance_date': self.acceptance_date.isoformat() if self.acceptance_date else None,
            'photo_receipt': self.photo_receipt,
            'photo_document_face': self.photo_document_face,
            'photo_document_back': self.photo_document_back,
            'scan_receipt': self.scan_receipt,
            'scan_document_face': self.scan_document_face,
            'scan_document_back': self.scan_document_back,
            'status': self.status.name,  # Если ContractStatus является Enum, используйте .name
        }


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
    
    # Добавляем метод serialize
    def serialize(self):
        return {
            'id': self.id,
            'contract_id': self.contract_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'sum': self.sum,
            'warranty': self.warranty,
        }


class Expense(db.Model):
    __tablename__ = 'expense'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    performer: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    sum: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    created_at: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime(timezone=True), 
        nullable=False
    )
    scan_receipt: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    
    def __repr__(self):
        return f'<Expense {self.name}, ID {self.id}, Date {self.created_at}>'
    
    # Добавляем метод serialize
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'performer': self.performer,
            'sum': self.sum,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'scan_receipt': self.scan_receipt,
        }


class API(db.Model):
    __tablename__ = 'api'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    created_by: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    created_at: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(moscow_tz)
    )
    last_request_at: so.Mapped[sa.DateTime] = so.mapped_column(
        sa.DateTime(timezone=True), 
        nullable=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), nullable=True)
    key: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    secret_key: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)

    def __repr__(self):
        return f'<API ID {self.id}, Created By {self.created_by}, Date {self.created_at}>'

    # Добавляем метод serialize
    def serialize(self):
        return {
            'id': self.id,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_request_at': self.last_request_at.isoformat() if self.last_request_at else None,
            'description': self.description,
            'key': self.key,
            'secret_key': self.secret_key,
        }
