import os
from termcolor import colored

from flask import Flask
from flask_cors import CORS
from sqlalchemy_utils import database_exists, create_database, drop_database

from .config import app_config
from .models import db, bcrypt

from .views.auth_view import auth
from .views.dadata_view import dadata

DB_URL = os.environ['DATABASE_URL']

def create_app(testing=False):
    app = Flask(__name__)

    CORS(app)

    if testing:
        app.config.from_object(app_config['testing'])
    else:
        env_name = os.environ['FLASK_ENV']
        app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(dadata)

    @app.route('/', methods=['GET'])
    def index():
        return 'Congratulations! Your first endpoint is working'


    @app.cli.command('resetdb')
    def resetdb_command():
        """
        Destroys and creates the database + tables.
        from https://vsupalov.com/flask-sqlalchemy-postgres/
        """

        if database_exists(DB_URL):
            print('Deleting database.')
            drop_database(DB_URL)
        if not database_exists(DB_URL):
            print('Creating database.')
            create_database(DB_URL)

        print('Creating tables.')
        db.create_all()
        print(colored('Database ready!', 'green'))

    return app