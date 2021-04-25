from flask import current_app
from .. import db
from app import getShortID

from sqlalchemy import text

class Item(db.Model):
    __tablename__ = 'items'
    sku = db.Column(db.Unicode(length=5), unique=True, primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(precision=10, scale=2))
    location = db.Column(db.Unicode(length=1))
    living = db.Column(db.Boolean())
    __mapper_args__ = {'polymorphic_on': living}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sku = getShortID()

    def supplier(self):
        sql = text("SELECT supplier FROM orders WHERE item = '{}'".format(self.sku))
        result = db.session.execute(sql).scalar()
        return str(result)

    def supplierName(self):
        sql = text("SELECT name FROM suppliers WHERE id = '{}'".format(self.supplier()))
        result = db.session.execute(sql).scalar()
        return str(result)

    def dateRec(self):
        sql = text("SELECT date_received FROM orders WHERE item = '{}'".format(self.sku))
        result = db.session.execute(sql).scalar()
        return result

    #def getName(self):
    #    sql = text("SELECT FROM orders WHERE item = '{}'".format(self.sku))
    #    result = db.session.execute(sql).scalar()
    #    return result

    def updateQty(self, amnt):
        if int(amnt) < 0:
            newQ = self.quantity + amnt
            if newQ >= 0:
                self.quantity = newQ
            else:
                return "[{}] Error: only {} in stock".format(self.sku, self.quantity)
        elif int(amnt) > 0:
            self.quantity += amnt
            return "[{}] Update successful".format(self.sku)
        else:
            return "Done. (No change)"

    def __repr__(self):
        return '<Item \'%s\'>' % self.sku


class Product(Item):
    __tablename__ = 'products'
    __mapper_args__ = {'polymorphic_identity': False}
    sku = db.Column(db.Unicode(length=5),
                    db.ForeignKey('items.sku'),
                    unique=True, 
                    primary_key=True
                    )
    name = db.Column(db.Unicode(length=64))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sku = getShortID()

    def getName(self):
        return str(self.name)
    
    def __repr__(self):
        return '<Product \'%s\'>' % self.sku
