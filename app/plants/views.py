from flask import ( Blueprint, abort, flash,redirect, render_template, request,url_for, make_response)
from app.models import (Family, Genus, Species, Variety, Plant, Medium, Item, Orders, WaterLog)
from app import db, dprint, printSQL
from app.plants.forms import (PlantSearchForm, SelectForm, plantForm, plantInventoryForm, SpeciesForm, VarietyForm, waterForm, TaxonForm, substrateForm)

from wtforms.fields import (SelectField, StringField,)
from wtforms.widgets import HiddenInput
from flask.views import MethodView
from flask_login import login_required, current_user
from app.decorators import admin_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc, func, update

import json, sys, random, datetime
from datetime import date, timedelta
import decimal

plants = Blueprint('plants', __name__)

import shamrock
from shamrock import Shamrock

#########################################


def parseTrefle(plantName):
    api = Shamrock('Yw9dZYtMjWDqe5SYEPcxB7vO7VHU3t08cC_T9vNKlDQ')
    result = api.search(plantName)
    list = []
    for count, item in enumerate(result['data']):
        try:
            list.append(
                (int(item['id']),
                str('(' + item['family'] + ') ' + item['scientific_name']))
                )
        except:
            list.append((int(item['id']), str(item['scientific_name'])))
    return list

def getSpecie(plantID):
    api = Shamrock('Yw9dZYtMjWDqe5SYEPcxB7vO7VHU3t08cC_T9vNKlDQ')
    result = api.plants(plantID)
    return result


@plants.route('/_get_genera/<int:famID>', methods=['GET'])
def get_genera(famID):
    """
	Return a list of 2-tuples (<genus id>, <genus name>)
	"""
    data = {}
    for entry in Genus.query.filter_by(family=famID).all():
        data[entry.id] = entry.name
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@plants.route('/_get_species/<int:genID>', methods=['GET'])
def get_species(genID):
    """
	Return a list of 2-tuples (<species id>, <species name>)
	"""
    data = {}
    for entry in Species.query.filter_by(genus=genID).all():
        data[entry.id] = entry.name
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@plants.route('/_get_varieties/<int:speID>', methods=['GET'])
def get_varieties(speID):
    """
	Return a list of 2-tuples (<variety id>, <variety name>)
	"""
    data = {}
    for entry in Variety.query.filter_by(species=speID).all():
        data[entry.id] = entry.name
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@plants.route('/_short_name/<SKU>', methods=['GET'])
def get_shortName(SKU):
    """
	Return a string containing the abbreviated species name (e.g. F. lyrata)
	"""
    plant = Plant.query.filter(Plant.sku == SKU).first()
    return plant.shortName()


@plants.route('/_full_name/<SKU>', methods=['GET'])
def get_fullName(SKU):
    """
	Return a string containing the abbreviated species name (e.g. F. lyrata)
	"""
    plant = Plant.query.filter_by(sku=SKU).first()
    return plant.fullName()


########################
# Add species from trefle.io
# 1/2
@plants.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = PlantSearchForm()
    if form.validate_on_submit():
        plantName = form.plantName.data
        return redirect(url_for('plants.select', plantName=plantName))
    return render_template('plants/search.html', form=form)
# Select species from list
# 2/2
@plants.route('/plant-search/<plantName>', methods=['GET', 'POST'])
@login_required
def select(plantName):
    """Select from list of species"""
    form = SelectForm()
    form.plantInfo.choices = parseTrefle(plantName)
    if form.validate_on_submit():
        plantID = form.plantInfo.data
        if db.session.query(db.exists().where(Species.id == plantID)).scalar():
            taxon = db.session.query(Species, Genus).join(
                Genus,
                Genus.id == Species.genus).filter(Species.id == plantID).one()
            flash(
                'Entry for <i>{} {}</i> (ID#{}) already exists in database'.
                format(taxon.Genus.name.capitalize(), taxon.Species.name,
                       plantID), 'form-error')
        # add database stuff
        else:
            result = getSpecie(plantID)
            sName = result['data']['scientific_name'].split()

            family = Family(id=int(result['data']['family']['id']),
                            name=result['data']['family']['name'])
            genus = Genus(
                id=int(result['data']['genus']['id']),
                name=result['data']['genus']['name'],
                family=int(result['data']['family']['id']),
            )
            species = Species(id=int(plantID),
                              name=sName[-1],
                              genus=int(result['data']['genus']['id']))
            if not db.session.query(
                    db.exists().where(Family.id == family.id)).scalar():
                db.session.add(family)
                db.session.commit()
            if not db.session.query(
                    db.exists().where(Genus.id == genus.id)).scalar():
                db.session.add(genus)
                db.session.commit()
            if not db.session.query(
                    db.exists().where(Species.id == species.id)).scalar():
                db.session.add(species)
                db.session.commit()
            flash(
                '<i>{}</i> successfully added to plantDB'.format( species.shortName()), 'form-success' )
    return render_template('plants/select.html', form=form)


# Taxon DB
@plants.route('/add-species', methods=['GET', 'POST'])
@login_required
@admin_required
def add_species():
    title = "Add new species"
    sub = "manually add new species to database"
    form = SpeciesForm()

    famChoices = [
        ('0', '--- Select one ---'),
    ]
    for entry in Family.query.all():
        data = (entry.id, entry.name)
        famChoices.append(data)
    form.family.choices = famChoices
    form.family.coerce = int
    form.family.id = 'family_select'

    genChoices = [
        ('0', '------'),
    ]
    form.genus.choices = genChoices
    form.genus.coerce = int
    form.genus.id = 'genus_select'

    if form.is_submitted():
        # Check species, add if it doesn't already exist
        plant = Species(genus=form.genus.data,
                        name=form.species.data.lower(),
                        id=99999900 + random.randint(0, 99))

        if not db.session.query( \
                    db.exists()\
                    .where(Species.name == plant.name))\
                .scalar():
            db.session.add(plant)
            db.session.commit()
            db.session.refresh(plant)
            flash( '<i>{}</i> successfully added to plantDB'.format(
                    plant.shortName()), 'form-success')
        else:
            dbPlant = db.session.query(Species).filter(
                Species.name == plant.name).one()
            flash( '<i>{}</i> (ID#{}) already exists'.format(
                    plant.shortName(), plant.id), 'form-error')
    return render_template('plants/new_taxon.html',
                            form=form,
                            title=title,
                            sub=sub)

# Taxon DB
@plants.route('/add-variety', methods=['GET', 'POST'])
@login_required
@admin_required
def add_variety():
    title = "Add new cultivar"
    sub = "manually add new species variety to database"
    form = VarietyForm()

    famChoices = [
        ('0', '--- Select one ---'),
    ]
    for entry in Family.query.all():
        data = (entry.id, entry.name)
        famChoices.append(data)
    form.family.choices = famChoices
    form.family.coerce = int
    form.family.id = 'family_select'

    genChoices = [
        ('0', '------'),
    ]
    form.genus.choices = genChoices
    form.genus.coerce = int
    form.genus.id = 'genus_select'

    speChoices = [
        ('0', '------'),
    ]
    form.species.choices = speChoices
    form.species.coerce = int
    form.species.id = 'species_select'

    if form.is_submitted():
        plant = Variety(
            species=form.species.data,
            name=form.variety.data,
        )
        if not db.session.query(
                db.exists().where(Variety.name == plant.name)).scalar():
            db.session.add(plant)
            db.session.commit()
            db.session.refresh(plant)
            flash( '<i>{}</i> successfully added to plantDB'.format(
                    plant.shortName()), 'form-success')
        else:
            plantVar = db.session.query(Variety).filter(
                Variety.name == form.variety.data).scalar()
            flash('<i>{}</i> already exists'.format(plantVar.shortName()),
                  'form-error')

    return render_template('plants/new_taxon.html',
                            form=form,
                            title=title,
                            sub=sub)

# Inventory DB
# Add new plant inventory
# TaxonDB -> InventoryDB
@plants.route('/new-plant', methods=['GET', 'POST'])
@login_required
def new_plant():
    form = plantForm()

    choices = [('0', '--- Select one ---'),]
    for entry in Family.query.all():
        data = (entry.id, entry.name)
        choices.append(data)
    form.family.choices = choices

    choices = [ ('0', '--- Select one ---'), ]
    for entry in Medium.query.all():
        data = (entry.id, entry.name)
        choices.append(data)
    form.substrate.choices = choices

    if form.is_submitted():
        plant = Plant(
            species=form.species.data,
            size=form.size.data,
            substrate=form.substrate.data,
        )
        if form.variety.data is not 0:
            plant.variety = form.variety.data
        
        db.session.add(plant)
        db.session.commit()
        db.session.refresh(plant)

        flash(
            'SKU: {} | <i>{}</i> successfully added to inventory'.format(
                plant.sku, plant.shortName()), 'form-success')


    return render_template('plants/new_item.html', form=form)


@plants.route('/new-plant2', methods=['GET', 'POST'])
@plants.route('/new-plant2/', methods=['GET', 'POST'])
@login_required
def new_plant2():
    return redirect(url_for('plants.new_plant2_edit', SKU=0))


# Inventory DB
@plants.route('/add', methods=['GET', 'POST'])
@plants.route('/add/', methods=['GET', 'POST'])
@login_required
def add_inv():
    return redirect(url_for('plants.edit_inv', SKU=0))
@plants.route('/edit/<SKU>', methods=['GET', 'POST'])
@login_required
def edit_inv(SKU):
    form = plantForm()
    success = False

    choices = [('0', '--- Select one ---'),]
    for entry in Family.query.all():
        data = (entry.id, entry.name)
        choices.append(data)
    form.family.choices = choices

    choices = [('0', '--- Select one ---'),]
    for entry in Medium.query.all():
        data = (entry.id, entry.name)
        choices.append(data)
    form.substrate.choices = choices

    choices = [('0', '--- Select one ---'),]
    for entry in Plant.query.all():
        data = (entry.sku, '[{}] {} - {}"'.format(entry.sku, entry.shortName(), entry.size))
        choices.append(data)
    form.parent.choices = choices


    if SKU != '0':
        # If sku != 0, pre-fill form
        item = db.session.query(Plant).filter_by(sku=SKU).first()
        title = 'Edit'
        sub = 'Editing entry for plant <{}>'.format(item.sku)

        genChoices = []
        for entry in Genus.query.all():
            data = (entry.id, entry.name)
            genChoices.append(data)

        speChoices = []
        for entry in Species.query.all():
            data = (entry.id, entry.name)
            speChoices.append(data)
        form.species.choices = speChoices

        parChoices = []
        for entry in Plant.query.filter_by(species=item.species).all():
            data = (entry.sku, '[{}] {} - {}"'.format(entry.sku, entry.shortName(), entry.size))
            parChoices.append(data)
        form.parent.choices = parChoices

        form.family.data = item.family()
        form.genus.data = item.genus()
        form.species.data = item.species
        form.parent.data = item.parent
        form.size.data = item.size
        form.substrate.data = item.substrate
        form.date_received.data = item.date_received


        if item.variety is not None:
            varChoices = []
            for entry in Variety.query.filter_by(species=item.species).all():
                data = (entry.id, entry.name)
                varChoices.append(data)
            form.variety.choices = varChoices
            form.variety.data = 0

    else:
        # If SKU = 0, then present form to add new plant
        title = 'Add New Plant to Inventory'
        sub = 'Select species from database'

        if request.method == "POST":
            item = Plant(
                species = request.form['species'],
                size = request.form['size'],
                substrate = request.form['substrate'],
                user = current_user.id,
                date_received = request.form['date_received']
            )

            dprint(request.form['date_received'])


            if form.variety.data is not '0':
                item.variety = request.form['variety']
            else:
                item.variety = None

            if form.parent.data is not 0:
                item.parent = request.form['parent']

            db.session.add(item)
            try:
                db.session.commit()
            except:
                flash('Problem adding plant to inventory'.format(
                        item.sku, item.shortName()), 'form-error')
            else:
                flash('SKU: {} | <i>{}</i> successfully added to inventory'.format(
                        item.sku, item.shortName()), 'form-success')

            return redirect(url_for('plants.edit_inv', SKU=item.sku))

    if request.method == "POST":
        dprint(request.form['date_received'])
        dprint(current_user)
        item.species=request.form['species']
        item.size=request.form['size']
        item.substrate=request.form['substrate']
        item.date_received=request.form['date_received']
        item.sku = SKU

        dprint(type(request.form['parent']))


        if request.form['variety'] is not '0':
            item.variety=request.form['variety']
        else:
            item.variety = None
        if request.form['parent'] is not 0:
            item.parent = request.form['parent']
        else:
            item.parent = None
        db.session.commit()
        dprint(item.__dict__)

        success = True

        flash('SKU: {} | <i>{}</i> successfully updated'.format(
                    item.sku, item.shortName()), 'form-success')
        return redirect(url_for('plants.edit_inv', SKU=item.sku))

    return render_template("plants/new_item.html", form=form, success=success, title=title, sub=sub)


@plants.route('/log/<sku>', methods=['GET', 'POST'])
@login_required
def logEntry(sku):
    """
	Add notes per-specimen about watering, feeding, or other 
	"""
    plant = Plant.query.filter(Plant.sku == sku).first()
    plantNotes = {}
    try:
        logQuery = WaterLog.query.filter(WaterLog.plant == sku).order_by(
            desc('date'))

        lastFeed = logQuery.filter(WaterLog.feed == 1).first()
        lastWater = logQuery.filter(WaterLog.water == 1).first()
        lastEvents = logQuery.all()
    except:
        lastWater = 'No data'
        lastFeed = 'No data'
    else:
        if bool(lastWater):
            lastWater = str(lastWater.date)
        if bool(lastFeed):
            lastFeed = str(lastFeed.date)
        for event in lastEvents:
            if bool(event.notes):
                if len(event.notes) > 0:
                    plantNotes[event.date] = event.notes

    form = waterForm()

    if form.is_submitted():
        if form.validate():
            logEntry = WaterLog(plant=str(sku),
                                water=form.water.data,
                                feed=form.feed.data,
                                date=form.date.data,
                                notes=form.notes.data)
            try:
                db.session.add(logEntry)
                db.session.commit()
            except:
                flash('Failed to add log entry', 'form-warning')
            else:
                flash('Log entry added', 'form-success')

    form.date.data = date.today()
    var = dict([('plant', plant.shortName()), ('water', lastWater),
                ('feed', lastFeed), ('id', sku)])
    return render_template("plants/log.html",
                           notes=plantNotes,
                           var=var,
                           form=form,
                           numNotes=len(plantNotes))
    #plantName=plant.fullName(), id=plant.sku, lastWater=lastWater, lastFeed=lastFeed, form=form


@plants.route('/log/all', methods=['GET', 'POST'])
def massWater():

    families = Family.query.all()
    plantQu = Plant.query.all()

    water = False
    feed = False
    notes = ''
    plantList = []
    addEntry=0

    if request.method == "POST":
        for i in request.form:
            if i == 'water':
                water = True
            elif i == 'feed':
                feed = True
            elif i == 'csrf_token':
                pass
            elif i == 'submit':
                pass
            elif i == 'notes':
                if request.form[i].__hash__() is not 0:
                    notes = request.form[i].__str__()
            else:
                plantList.append(i)
                dprint('Plant: ',i)
                
        if plantList.__len__() == 0:
            flash('No plants selected', 'form-error')
        elif water == False and feed == False:
            if len(notes.strip()) == 0:
                flash('Nothing to add', 'form-error')
            else:
                addEntry=1
        else:
            addEntry=1

    if addEntry != 0:
        for i in plantList:
            logEntry = WaterLog(plant=i,
                water=water,
                feed=feed,
                date=date.today(),
                notes=notes)
            try:
                db.session.add(logEntry)
                db.session.commit()
            except:
                flash('Failed to add log entry', 'form-warning')
            else:
                flash('Added to log', 'form-success')


    return render_template('plants/mass-water.html',
        plants=plantQu,
        families=families,
        form=TaxonForm() )


@plants.route('/water', methods=['GET', 'POST'])
@login_required
def water():
    """
	calendar-style watering display 
	"""
    calendar = {}
    startDate = date.today() - timedelta(days=21)
    row2 = [0] * 15
    for a in range(15):
        row2[a] = (startDate + timedelta(days=a + 7)).day

    waterPlants = []
    plantNames = {}
    dateCol = startDate
    currentPlants = db.session.query(WaterLog.plant.distinct()).filter(
        WaterLog.date >= dateCol).order_by(asc('date'))
    note = False
    for i in currentPlants.all():
        plantNames[i[0]] = Plant.query.filter(Plant.sku == i[0]).first()
        dateCol = startDate
        plantCal = [0] * 22

        event = db.session.query(WaterLog).filter(
            WaterLog.plant == i[0]).order_by(asc('date'))
        nextEvent = event.filter(WaterLog.date >= dateCol).first()
        watr = 0

        for j in range(22):
            note = False
            if watr > 0:
                watr -= 1
            if nextEvent.date > dateCol:
                if watr < 0:
                    watr = 0
            elif nextEvent.date == dateCol:
                if nextEvent.water == 1:
                    watr = 7
                note = True
                event2 = event.filter(WaterLog.date > dateCol).first()
                if event2 != None:
                    nextEvent = event2
            else:
                pass
            plantCal[j] = (note, 'b{}'.format(watr))
            dateCol += timedelta(days=1)
        calendar[i[0]] = plantCal[7:]

    return render_template("plants/water.html",
                           date=date.today(),
                           startDate=startDate,
                           row2=row2,
                           calendar=calendar,
                           shortName=plantNames)


@plants.route('/add/substrate', methods=['GET', 'POST'])
def add_substrate():
    form = substrateForm()
    if form.validate_on_submit():
        medium = Medium(
            name = form.name.data,
            notes = form.notes.data
        )
        db.session.add(medium)
        try:
            db.session.commit()
        except:
            dprint('whoops')
        else:
            return redirect(url_for('main.index'))
    return render_template("plants/new-medium.html", form=form)

@plants.route('/inventory')
def inventory():

    families = db.session.query(Family).all()
    plantQu = Plant.query.all()

    varieties = {}
    for i in db.session.query(Variety).all():
        varieties[i.species] = i.name

    return render_template('plants/inventory.html',
                           plants=plantQu,
                           families=families,
                           varieties=varieties)
