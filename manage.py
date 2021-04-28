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
from app.models import Role, Employee, Plant, WaterLog, Species, Genus, Family, Plant
from config import Config

from datetime import datetime, date, timedelta
from random import randrange, choice

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, 
        db=db, 
        Employee=Employee, Role=Role, 
        Plant=Plant, WaterLog=WaterLog, 
        Species=Species, Genus=Genus, Family=Family
        )


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
