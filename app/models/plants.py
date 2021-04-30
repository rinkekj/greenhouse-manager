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
    family = db.Column(db.Integer, db.ForeignKey('families.id'), nullable=False)
    name = db.Column(db.Unicode(length=25), unique=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Genus \'%s\'>' % self.name

class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    genus = db.Column(db.Integer, db.ForeignKey('genera.id'), nullable=False)
    name = db.Column(db.Unicode(length=25), unique=False, nullable=False)

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
    id = db.Column(
                    db.Unicode(length=5),
                    primary_key=True,
                    unique=True,
                    nullable=False)
    species = db.Column(
                    db.Integer,
                    db.ForeignKey('species.id'),
                    nullable=False)
    name = db.Column(db.Unicode(length=50), nullable=False)


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
#	Substrates
##########################################################
class Medium(db.Model):
    __tablename__ = 'substrates'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.Unicode(length=25), unique=False, nullable=False)
    notes = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Medium \'{}\'>'.format(self.name)

##########################################################
#	Physical inventory (plants, merchandise
##########################################################
class Plant(db.Model):
    __tablename__ = 'plants'
    #__mapper_args__ = {'polymorphic_identity': True}
    sku = db.Column(db.Unicode(length=5),
                    unique=True, 
                    primary_key=True
                    )
    species = db.Column(db.Integer,
                    db.ForeignKey('species.id'),
                    )
    variety = db.Column(db.Unicode(length=5),
                    db.ForeignKey('varieties.id'),
                    nullable=True
                    )
    size = db.Column(db.Integer)
    user = db.Column(db.Integer, 
                    db.ForeignKey('employees.id'),
                    )
    date_received = db.Column(db.Date)
    substrate = db.Column(db.Integer,
                    db.ForeignKey('substrates.id'),
                    )
    parent = db.Column(db.Unicode(length=5),
                    db.ForeignKey('plants.sku'),
                    nullable=True
                    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sku = getShortID()

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
