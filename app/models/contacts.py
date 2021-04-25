from flask import current_app
from .. import db
from app import getShortID, dprint
import random
import phonenumbers

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Unicode(length=5), primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(length=64), index=True, nullable=False)
    last_name = db.Column(db.String(length=64), index=True, nullable=False)
    email = db.Column(db.String(length=64), unique=True, index=True)
    phone = db.Column(db.BigInteger(), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = getShortID()

    def fullName(self):
        return '%s %s' % (self.first_name, self.last_name)

    def printNum(self):
        try:
            pNum = phonenumbers.parse( str(self.phone), "US")
        except:
            return ''
        else:
            return phonenumbers.format_number( pNum, phonenumbers.PhoneNumberFormat.NATIONAL )

    def __repr__(self):
        return '<Contact \'%s\'>' % self.fullName()

    def parseNum(self, phoneNum):
        try:
            pNum = phonenumbers.parse( str(phoneNum), "US")
        except:
            return ''
        else:
            return int(pNum.national_number)

    @staticmethod
    def generate_fake(count=100, **kwargs):
        #Generate fake customers for demo
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker
        from faker_e164.providers import E164Provider
        import phonenumbers

        fake = Faker()
        fake.add_provider(E164Provider)

        seed()
        for i in range(count):
            x = phonenumbers.parse( fake.e164(
                            region_code="US", 
                            valid=True, 
                            possible=True), 
                            "US")
            phoneNum = str( phonenumbers\
                    .format_number( x, phonenumbers.PhoneNumberFormat.NATIONAL))
            phoneNum = phoneNum.replace(" ", "")
            phoneNum = phoneNum.replace("(", "")
            phoneNum = phoneNum.replace(")", "")
            phoneNum = phoneNum.replace("-", "")
            c = Contact(first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.email(),
                        phone=phoneNum,
                        **kwargs)
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Unicode(length=5), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.Unicode(length=50), unique=True, nullable=False)
    address = db.Column(db.Unicode(length=50))
    city = db.Column(db.String(length=20))
    state = db.Column(db.String(length=2))
    zip = db.Column(db.Integer())
    contact = db.Column(db.Unicode(length=5),
                        db.ForeignKey('contacts.id'),
                        nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = getShortID()

    def __repr__(self):
        return '<Supplier \'%s\'>' % self.name
