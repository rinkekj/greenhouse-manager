from .. import db
from datetime import datetime
import sys
from app.models.contacts import Supplier
from app import getShortID, dprint
from sqlalchemy import text


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Unicode(length=5), primary_key=True)
    item = db.Column(db.Unicode(length=5), primary_key=True)
    qty = db.Column(db.Integer)
    price = db.Column(db.Numeric(precision=10, scale=2))
    date = db.Column(db.Date)
    date_received = db.Column(db.Date)
    supplier = db.Column(db.Unicode(length=5),
            db.ForeignKey('suppliers.id'),
            nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = getShortID()

    def __repr__(self):
        return '<Order \'%s\'>' % self.id

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Unicode(length=5), primary_key=True)
    date = db.Column(db.Date)
    customer = db.Column(db.Unicode(length=5),
            db.ForeignKey('contacts.id'),
            nullable=False)
    item = db.Column(db.Unicode(length=5), primary_key=True)
    qty = db.Column(db.Integer)
    salePrice = db.Column(db.Numeric(precision=10, scale=2))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = getShortID()

    def __repr__(self):
        return '<Sale \'%s\'>' % self.id