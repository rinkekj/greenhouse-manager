from .. import db
from datetime import datetime
import sys
from app import dprint, getShortID, printSQL
from app.models.contacts import Supplier
from app.models.stock import Item
import random
from sqlalchemy import desc, text

##########################################################
#	Taxonomic information
##########################################################
class Family(db.Model):
    __tablename__ = 'families'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.Unicode(length=25), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Family \'%s\'>' % self.name

class Genus(db.Model):
    __tablename__ = 'genera'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.Unicode(length=25), unique=False)
    family = db.Column(db.Integer, db.ForeignKey('families.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Genus \'%s\'>' % self.name

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.Unicode(length=25), unique=False, nullable=False)
    genus = db.Column(db.Integer, db.ForeignKey('genera.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fullName(self):
        genN = db.session.query(Genus.name).filter_by(id=self.genus).scalar()
        return '%s %s' % (genN.capitalize(), self.name)

    def shortName(self):
        genN = db.session.query(Genus.name).filter_by(id=self.genus).scalar()
        return '%s. %s' % (genN[0].upper(), self.name)

    def __repr__(self):
        return '<Species \'%s\'>' % self.shortName()

class Variety(db.Model):
    __tablename__ = 'varieties'
    id = db.Column(db.Unicode(length=5),
                   primary_key=True,
                   unique=True,
                   nullable=False)
    name = db.Column(db.Unicode(length=50), nullable=False)
    species = db.Column(db.Integer,
                        db.ForeignKey('species.id'),
                        nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = getShortID()

    def fullName(self):
        varQ = db.session.query(Species, Genus)\
            .join(Genus,Genus.id == Species.genus)\
            .filter(Species.id == self.species)
        taxon = varQ.one()
        return '%s %s var. %s' % (taxon.Genus.name.capitalize(),
                                  taxon.Species.name, self.name)

    def shortName(self):
        varQ = db.session.query(Species, Genus)\
            .join(Genus,Genus.id == Species.genus)\
            .filter(Species.id == self.species)
        taxon = varQ.one()
        return '%s. %s var. %s' % (taxon.Genus.name[0].upper(),
                                   taxon.Species.name, self.name)

    def __repr__(self):
        return '<Variety \'%s\'>' % self.name

##########################################################
#	Physical inventory (plants, merchandise
##########################################################
class Plant(Item):
    __tablename__ = 'plants'
    __mapper_args__ = {'polymorphic_identity': True}
    sku = db.Column(db.Unicode(length=5),
                    db.ForeignKey('items.sku'),
                    unique=True, 
                    primary_key=True
                    )
    species = db.Column(db.Integer,db.ForeignKey('species.id'))
    variety = db.Column(db.Unicode(length=5), db.ForeignKey('varieties.id'))
    size = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sku = getShortID()
        self.living = True

    def family(self):
        famID = db.session.query(Genus.family)\
            .filter_by(id=db.session\
                .query( Species.genus )\
                .filter_by( id=self.species )\
                .scalar() )\
            .scalar()
        return famID

    def familyName(self):
        sql = text("SELECT name FROM families WHERE id = '{}'".format(self.family()))
        resp = str(db.session.execute(sql).scalar())
        return resp

        #famName = db.session.query( Family.name ).filter_by( id=self.family() ).scalar()
        #return famName

    def genus(self):
        sql = text("SELECT genus FROM species WHERE id = '{}'".format(self.species))
        resp = str(db.session.execute(sql).scalar())
        return resp
        
        #genID = db.session.query( Species.genus ).filter_by(id=self.species).scalar()
        #return genID

    def genusName(self):
        sql1 = text("SELECT genus FROM species WHERE id = '{}'".format(self.species))
        sql2 = text("SELECT name FROM genera WHERE id = '{}'".format( db.session.execute(sql1).scalar() ))
        resp = str(db.session.execute(sql2).scalar())
        return resp

    def speciesName(self):
        sql = text("SELECT name FROM species WHERE id = '{}'".format(self.species))
        resp = db.session.execute(sql).scalar()
        return resp

        #speName = db.session.query( Species.name ).filter_by( id=self.species ).scalar()
        #return speName

    def varietyName(self):
        if self.variety:
            sql = text("SELECT name FROM varieties WHERE species = '{}'".format(self.species))
            resp = db.session.execute(sql).scalar()
            return resp
            #varName = db.session.query( Variety.name ).filter_by( id=self.species ).scalar()
            #return str(varName)
        else:
            return ''

    def shortName(self):
        genName = self.genusName()
        specName = self.speciesName()

        if self.variety:
            varName = db.session.query(Variety.name).filter_by(id=self.variety).scalar()
            return '{}. {} var. {}'.format(genName[0].upper(), specName, varName)
        else:
            return '{}. {}'.format(genName[0].upper(), specName)

    def fullName(self):
        if self.variety is not None:
            varietyName = db.session.query(
                Variety.name).filter_by(id=self.variety).scalar()
            return '{} {} var. {}'.format(self.genusName().capitalize(), self.speciesName(), varietyName)
        else:
            return '{} {}'.format(self.genusName().capitalize(), self.speciesName())

    def getName(self):
        return str(self.shortName())

    def lastWater(self):
        wDate = db.session\
            .query(WaterLog.date)\
            .order_by(desc('date'))\
            .filter_by( plant=self.sku )\
            .first()
        return wDate[0].strftime("%Y-%m-%d")
    def getName(self):
        return self.shortName()

    def __repr__(self):
        return '<Plant \'{}\'>'.format(self.sku)

    @staticmethod
    def generate_fake(count, **kwargs):
        """Generate a number of fake users for testing."""
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice, randrange
        from faker import Faker

        zones = {'A': (32,218), 
                 'B': (45,65,495),
                 'C': (69,149),
                 'D': (54,616)
                 }

        fake = Faker()
        seed()

        varietiesAvailable = db.session\
            .query(Species.id, Variety.id)\
            .join(Species, Species.id == Variety.species)\
            .all()

        speciesAvailable = db.session\
            .query(Species.id)\
            .all()
        plants = []
        plantsCreated = []
        for i in varietiesAvailable:
            plants.append(i)
        for j in speciesAvailable:
            rand = j
            plants.append(rand)
        for i in range(count):
            randPlant = plants[randrange(1, len(plants), 1)]

            p = Plant(**kwargs)
            p.size = randrange(3, 12, 1)
            p.quantity = randrange(5, 25, 5)

            if len(randPlant) == 2:
                p.species = randPlant[0]
                p.variety = randPlant[1]
            else:
                p.species = randPlant.id

            if p.size >= 7:
                p.price = randrange(19, 59, 1) + 0.99
            else:
                p.price = randrange(4, 20, 2) + 0.99

            db.session.add(p)
            
            fam = p.family()
            for z in zones:
                if fam in zones[z]:
                    p.location = z
                    break            
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            else:
                plantsCreated.append(p)
        return plantsCreated

##########################################################
#	Watering Log
##########################################################
class WaterLog(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    plant = db.Column(db.Unicode(length=5),
                      db.ForeignKey('plants.sku'),
                      nullable=False)
    water = db.Column(db.Boolean, nullable=False)
    feed = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

    def __repr__(self):
        return '<WateringEvent \'%s\'>' % self.id
