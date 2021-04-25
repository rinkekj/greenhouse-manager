from __future__ import print_function
import os, sys

from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy, get_debug_queries
from flask_wtf import CSRFProtect

from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()

# Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'

# debug console print shortcut
def dprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Generate 5-char unique ID
def getShortID():
    from shortuuid import ShortUUID
    return ShortUUID().random(length=5)

# Print SQL statement
def printSQL():
    dprint( get_debug_queries() )

def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    Config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .plants import plants as plants_blueprint
    app.register_blueprint(plants_blueprint, url_prefix='/plants')

    from .register import register as register_blueprint
    app.register_blueprint(register_blueprint, url_prefix='/customer')

    return app
