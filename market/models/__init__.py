import datetime
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, validates

from .mixins import TimestampMixin, CommentMixin, DeleteMixin
from .base import db
logger = logging.getLogger(__name__)


class MarketSupplyer(TimestampMixin, CommentMixin, DeleteMixin, db.Model):
    __tablename__ = "market_supplyer"
    id = db.Column(db.Integer, primary_key=True)
    supplyer_id = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    name_short = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(255), nullable=False)

    def __str__(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state')
        return str(d)

    def __repr__(self):
        return super().__str__()
    def todict(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state')
        return d

class MarketMerchandise(TimestampMixin, CommentMixin, DeleteMixin, db.Model):
    __tablename__ = "market_merchandise"
    id = db.Column(db.Integer, primary_key=True)
    merchandise_id = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    # supplyer.id foreign key
    unit_price = db.Column(db.String(255), nullable=False)
    supplyer_id = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __str__(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state')
        return str(d)

    def __repr__(self):
        return super().__str__()


class MarketStaff(TimestampMixin, CommentMixin, DeleteMixin, db.Model):
    __tablename__ = "market_staff"
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(255), nullable=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(255), nullable=False, default='default')
    telephone = db.Column(db.String(255), nullable=False, unique=True)
    salary = db.Column(db.String(255), nullable=True)

    def __str__(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state')
        d.pop('password_hash')
        return str(d)

    def __repr__(self):
        return super().__str__()

    def todict(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state')
        d.pop('password_hash')
        return d


class MarketOrderMain(TimestampMixin, CommentMixin, DeleteMixin, db.Model):
    __tablename__ = "market_order_main"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(255), nullable=False, unique=True)
    staff_id = db.Column(db.String(255), nullable=False)
    gross_quantity = db.Column(db.Integer, nullable=False)
    gross_price = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)

    def __str__(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state')
        return str(d)

    def __repr__(self):
        return super().__str__()


class MarketOrderDetail(TimestampMixin, CommentMixin, DeleteMixin, db.Model):
    __tablename__ = "market_order_detail"
    id = db.Column(db.Integer, primary_key=True)  # order_main.id foreign key
    # merchandise.id foreign key
    order_detail_id = db.Column(db.String(255), nullable=False, unique=True)
    order_id = db.Column(db.String(255), nullable=False)
    merchandise_id = db.Column(db.String(255), nullable=False)
    merchandise_quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.String(255), nullable=False)
    gross_price = db.Column(db.String(255), nullable=False)

    def __str__(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state')
        return str(d)

    def __repr__(self):
        return super().__str__()
