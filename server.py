import os
from termcolor import colored

from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

app = Flask(__name__)

DB_URL = os.environ['DATABASE_URL']

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
BCRYPT_LOG_ROUNDS = 15

db = SQLAlchemy(app)

from models import User, Auth

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/register', methods=['POST'])
def register_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    new_user = User(username=username, email=email)
    new_auth = Auth(email=email, plaintext_password=password)

    db.session.add(new_user)
    db.session.add(new_auth)

    try:
        db.session.commit()
        return jsonify({ 'username': username, 'email': email })
    except IntegrityError:
        db.session.rollback()
        return jsonify({ 'error': 'email already exists' }), 400


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user_entry = User.query.filter_by(username=username).first()

    if user_entry is None:
        return jsonify({ 'error': 'username does not exist' }), 400
    else:
        auth_entry = Auth.query.filter_by(email=user_entry.email).first()
        if auth_entry.is_correct_password(password):
            return jsonify({ 'result': 'logged in' })
        else:
            return jsonify({ 'error': 'wrong password' }), 400


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