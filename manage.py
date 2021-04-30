#!/usr/bin/env python
import os
import subprocess
import click
import csv
from flask_migrate import Migrate, MigrateCommand

from flask_script import Manager, Shell, Server

from redis import Redis
from rq import Connection, Queue, Worker
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from app import create_app, db, dprint
from app.models import Role, Employee, Plant, WaterLog, Variety, Species, Genus, Family, Plant, Medium
from config import Config

from datetime import datetime, date, timedelta
from random import randrange, choice

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, 
        Employee=Employee, Role=Role, 
        Plant=Plant, WaterLog=WaterLog, 
        Species=Species, Genus=Genus, Family=Family)


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
    db.session.execute('SET FOREIGN_KEY_CHECKS=1;')
    db.session.commit()

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
    #admin_query = Role.query.filter_by(name='Administrator')
    #if admin_query.first() is not None:
    #    if Employee.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
    #        user = Employee(first_name='Admin',
    #                    last_name='Account',
    #                    password=Config.ADMIN_PASSWORD,
    #                    email=Config.ADMIN_EMAIL)
    #        db.session.add(user)
    #        db.session.commit()
    #        print('Added administrator {}'.format(user.full_name()))


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


@manager.command
def backup():

    #################
    # User
    with open('data/user.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'first_name', 'last_name', 'email', 'password_hash', 'role_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for u in Employee.query.all():
            writer.writerow( {'id':u.id, 'first_name':u.first_name, 'last_name':u.last_name, 
                                'email':u.email, 'password_hash':u.password_hash, 'role_id':u.role_id} )

    #################
    #Taxonomy backup

    # Family
    with open('data/family.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for fam in Family.query.all():
            writer.writerow( {'id':fam.id, 'name':fam.name} )

    # Genus
    with open('data/genus.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'family', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for gen in Genus.query.all():
            writer.writerow( {'id':gen.id, 'family':gen.family, 'name':gen.name} )

    # Species
    with open('data/species.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'genus', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for spe in Species.query.all():
            writer.writerow( {'id':spe.id, 'genus':spe.genus, 'name':spe.name} )

    # Variety
    with open('data/variety.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'species', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for var in Variety.query.all():
            writer.writerow( {'id':var.id, 'species':var.species, 'name':var.name} )

    #################
    # Medium backup
    with open('data/medium.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for med in Medium.query.all():
            writer.writerow( {'id':med.id, 'name':med.name, 'notes':med.notes} )

    #################
    # Plant backup
    with open('data/plants.csv', 'w', newline='') as csvfile:
        fieldnames = ['sku', 'species', 'variety', 'size', 'user', 'date_received', 'substrate', 'parent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for plt in Plant.query.all():
            writer.writerow( {'sku':plt.sku, 'species':plt.species,
                              'variety':plt.variety, 'size':plt.size,
                              'user':plt.user, 'date_received':plt.date_received,
                              'substrate':plt.substrate, 'parent':plt.parent} )

    #################
    # Log backup
    with open('data/log.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'plant', 'water', 'feed', 'date', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for log in WaterLog.query.all():
            writer.writerow( {'id':log.id, 'plant':log.plant, 
                              'water':log.water, 'feed':log.feed, 
                              'date':log.date, 'notes':log.notes} )


@manager.command
def restore():

    with open('data/user.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            u = Employee(
                id = row['id'],
                first_name = row['first_name'],
                last_name = row['last_name'],
                email = row['email'],
                password_hash = row['password_hash'],
                role_id = row['role_id']
            )
            db.session.add(u)
        db.session.commit()

    with open('data/medium.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            m = Medium(
                id = row['id'],
                name = row['name'],
                notes = row['notes']
            )
            db.session.add(m)
        db.session.commit()

    with open('data/family.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            f = Family(
                id = row['id'],
                name = row['name']
            )
            db.session.add(f)
        db.session.commit()

    with open('data/genus.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            g = Genus(
                id = row['id'],
                family = row['family'],
                name = row['name']
            )
            db.session.add(g)
        db.session.commit()

    with open('data/species.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            s = Species(
                id = row['id'],
                genus = row['genus'],
                name = row['name']
            )
            db.session.add(s)
        db.session.commit()

    with open('data/variety.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            v = Variety(
                id = row['id'],
                species = row['species'],
                name = row['name']
            )
            db.session.add(v)
        db.session.commit()
    
    
    with open('data/plants.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = Plant(
                sku = row['sku'],
                species = row['species'],
                variety = row['variety'],
                size = row['size'],
                user = row['user'],
                date_received = row['date_received'],
                substrate = row['substrate'],
                parent = row['parent']
            )
            db.session.add(p)
        db.session.commit()



if __name__ == '__main__':
    manager.run()
