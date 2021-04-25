#!/usr/bin/env python
import os
import subprocess

from flask_migrate import Migrate, MigrateCommand

from flask_script import Manager, Shell, Server

from redis import Redis
from rq import Connection, Queue, Worker
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from app import create_app, db, dprint
from app.models import Role, Employee, Contact, Plant, Orders, Sales, WaterLog, Species, Genus, Supplier, Product, Item
from config import Config

from datetime import datetime, date, timedelta
from random import randrange, choice

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Employee=Employee, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0"))


# Zone A: Full shade, high humidity
# Zone B: Partial shade, high humidity
# Zone C: Partial shade, ambient humidity
# Zone D: Full sun, ambient humidity

@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.session.execute('SET FOREIGN_KEY_CHECKS=0;')
    db.session.execute('DROP TABLE IF EXISTS logs;')
    db.session.execute('DROP TABLE IF EXISTS employees;')
    db.session.execute('DROP TABLE IF EXISTS sales;')
    db.session.execute('DROP TABLE IF EXISTS plants;')
    db.session.execute('DROP TABLE IF EXISTS products;')
    db.session.execute('DROP TABLE IF EXISTS suppliers;')
    db.session.execute('DROP TABLE IF EXISTS orders;')
    db.session.execute('DROP TABLE IF EXISTS contacts;')
    db.session.execute('DROP TABLE IF EXISTS varieties;')
    db.session.execute('DROP TABLE IF EXISTS species;')
    db.session.execute('DROP TABLE IF EXISTS genera;')
    db.session.execute('DROP TABLE IF EXISTS families;')
    db.drop_all()
    db.create_all()
    db.session.commit()
    fakePlant = Plant(living = True)
    db.session.add(fakePlant)
    db.session.commit()
    db.session.delete(fakePlant)
    db.session.execute('SET FOREIGN_KEY_CHECKS=1;')
    db.session.commit()

@manager.command
def OrderMerchandise( numItems, orderDate, dayNum ):
    # Simulation
    # Generate fake order and add to inventory
    newOrder = Orders()
    StuffWeSell = [
        ('Shovel', 14.30, 24.99, 'B'),
        ('Peat moss - 5L', 4.75, 12.99, 'D'),
        ('Peat moss - 10L', 6.00, 19.99, 'D'),
        ('Perlite - 5L', 3.50, 10.99, 'D'),
        ('Perlite - 10L', 5.00, 16.99, 'D'),
        ('Hydroton - 10L', 7.31, 14.99, 'D'),
        ('Vermiculite - 5L', 3.75, 9.99, 'D'),
        ('Vermiculite - 10L', 5.75, 13.99, 'D'),
        ('"Premium" dirt - 5L', 0.50, 24.99, 'D'),
        ('Systemic granules', 7.50, 17.99, 'A'),
        ('Copper Fungicide', 11.45, 19.99, 'A'),
        ('Spray bottle', 0.75, 2.99, 'A'),
        ('Nursery pot - 3in', 0.25, 1.99, 'B'),
        ('Nursery pot - 6in', 0.35, 2.99, 'B'),
        ('Nursery pot - 9in', 0.45, 3.99, 'B')
        ]
    for item in StuffWeSell:
        newItem = Product(
            name = item[0],
            quantity = randrange(5,10,1),
            price = item[2],
            location = item[3],
        )
        invoice = Orders(
            item = newItem.sku,
            qty = newItem.quantity,
            price = item[1],
            date = orderDate,
            date_received = (orderDate + timedelta(days=2)),
            supplier = 'TAGda'
        )
        invoice.id = newOrder.id

        db.session.add(invoice)
        db.session.add(newItem)
        try:
            db.session.commit()
        except IntegrityError:
            dprint('uh oh')
            db.session.rollback()
        else:
            dprint("Day {}: Order[{}] Item[{}]".format(dayNum, invoice.id, invoice.item))



@manager.command
def OrderPlants( numPlants, orderDate, dayNum ):
    # Simulation
    # Generate fake plant order and add to inventory
    
    newOrder = Orders()
    
    plants = Plant.generate_fake( numPlants )
    for i in plants:
        invoice = Orders(
            supplier = 'TGKmf',
            date = orderDate,
            date_received = orderDate + timedelta(days=2),
            item = i.sku,
            price = i.price/randrange(2, 5, 1),
            qty = i.quantity
        )
        invoice.id = newOrder.id

        db.session.add(invoice)

        # Water plants when they arrive
        updateLog(i.sku, orderDate, dayNum)
        try:
            db.session.commit()
        except IntegrityError:
            dprint('uh oh')
            db.session.rollback()
        else:
            dprint("Day {}: Order[{}] Item[{}]".format( dayNum, invoice.id, invoice.item))

@manager.command
def updateLog(plantSKU, waterDate, dayNum):
    water = WaterLog(
            plant = plantSKU,
            water = 1,
            date = waterDate
        )
    f = randrange(0,2,1)
    if f == 1:
        water.feed = 1
        water.notes = "General purpose fertilizer; half-strength"
    else:
        water.feed = 0
    db.session.add(water)
    try:
        db.session.commit()
    except IntegrityError:
        dprint('uh oh')
        db.session.rollback()
    else:
        dprint("Day {}: LogEntry[{}] Plant[{}]".format(dayNum, water.id, water.plant))


@manager.command
def checkStock(simDay, dayNum):
    stock = Product.query.all()
    reOrder = Orders()
    for i in stock:
        if i.quantity == 0:
            newItem = Product(
                name = i.name,
                quantity = randrange(5,10,1),
                price = i.price,
                location = i.location,
            )
            invoice = Orders(
                item = newItem.sku,
                qty = newItem.quantity,
                price = newItem.price / 3,
                date = simDay,
                date_received = (simDay + timedelta(days=2)),
                supplier = 'TAGda'
            )

            invoice.id = reOrder.id
            db.session.delete(i)
            db.session.add(invoice)
            db.session.add(newItem)
            try:
                db.session.commit()
            except IntegrityError:
                dprint('uh oh')
                db.session.rollback()
            else:
                dprint("Day {}: Order[{}] Item[{}]".format(dayNum, invoice.id, invoice.item))

@manager.command
def waterPlants(simDay, dayNum):
    # Water simulated plants
    # Group plants by watering requirements
    
    simPlants = db.session.query(Plant).filter(Plant.quantity > 0).all()
    for i in simPlants:
        lastLog = db.session.query(WaterLog)\
                            .filter(WaterLog.plant == i.sku)\
                            .order_by(desc('date')).first()
        
        if i.location == 'A':
            if (simDay - lastLog.date) == timedelta(days=5):
                updateLog(i.sku, simDay, dayNum)
        elif i.location == 'B':
            if (simDay - lastLog.date) == timedelta(days=7):
                updateLog(i.sku, simDay, dayNum)
        else: 
            if (simDay - lastLog.date) >= timedelta(days=10):
                updateLog(i.sku, simDay, dayNum)

@manager.command
def add_fake_data():
    # Generate fake customers
    Contact.generate_fake(count=50)

    # All simulated customers are returning customers
    simContacts = db.session.query(Contact.id).all()

    # Simulate 60 days of slow, daily business
    simDay = date.today() - timedelta(days=60)
    dayNum = 0

    # Initial inventory
    OrderPlants(5, (simDay - timedelta(days=2)), dayNum)
    OrderMerchandise(5, (simDay - timedelta(days=2)), dayNum)

    # Begin simulation
    while (date.today() - simDay) > timedelta(days=0):
        waterPlants(simDay, dayNum)
        checkStock(simDay, dayNum)
        if (dayNum % 7) == 0:
            OrderPlants(5, (simDay - timedelta(days=2)), dayNum)

        # Between 2 and 5 customers per day, chosen at random
        # (It's ok, everything's overpriced)
        # Customers come in an buy a handful of random items
        # Sales are generated and added to DB
        # Inventory updates
        for i in range(1, randrange(2,5,1)):
            transactionID = Sales().id
            numItems = randrange(1,6,1)
            shopper = choice(simContacts)
            merch = []
            #plantsAvailable = Plant.query.all()
            itemsAvailable = Item.query.all()

            for item in itemsAvailable:
                merch.append(item)

            alreadyPicked = []
            for j in range(1, numItems):
                merchChoice = choice(merch)
                if merchChoice.sku in alreadyPicked:
                    pass
                elif merchChoice.quantity > 0:
                    multiplier = randrange(1,5,1)
                    cart = Sales(
                        id = transactionID,
                        date = simDay,
                        customer = shopper,
                        item = merchChoice.sku,
                        salePrice = merchChoice.price
                    )
                    # Check if we have enough of that item
                    if multiplier <= merchChoice.quantity:
                        cart.qty = multiplier
                    else:
                        cart.qty = 1
                    # Create entry in Sales
                    db.session.add(cart)
                    # Update quantities in Inventory DB
                    merchChoice.updateQty( -cart.qty )
                    # Don't pick the same item twice
                    alreadyPicked.append(cart.item)
                    dprint("Day {}: Customer[{}] purchased Item[{}]".format(dayNum, shopper, cart.item))
            try:
                db.session.commit()
            except IntegrityError:
                dprint('uh oh')
                db.session.rollback()

        # Advance simulation one day
        simDay += timedelta(days=1)
        dayNum += 1



@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()

@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()

def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    Role.insert_roles()
    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if Employee.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = Employee(first_name='Admin',
                        last_name='Account',
                        password=Config.ADMIN_PASSWORD,
                        email=Config.ADMIN_EMAIL)
            db.session.add(user)
            db.session.commit()
            print('Added administrator {}'.format(user.full_name()))


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listen = ['default']
    conn = Redis(host=app.config['RQ_DEFAULT_HOST'],
                 port=app.config['RQ_DEFAULT_PORT'],
                 db=0,
                 password=app.config['RQ_DEFAULT_PASSWORD'])

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()
