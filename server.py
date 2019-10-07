import os
import requests
from termcolor import colored

from flask import Flask, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DADATA_KEY = os.environ['DADATA_KEY']
DADATA_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/'
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
        return jsonify({ 
            'username': username, 
            'email': email, 
            'joined': new_user.joined_at 
        })
    except IntegrityError as error:
        db.session.rollback()
        if "users_username_key" in str(error):
            return jsonify({ 'error': 'username already exists' }), 400
        elif "email_key" in str(error):
            return jsonify({ 'error': 'email already exists' }), 400
        else:
            return jsonify({ 'error': 'unknown error' }), 400


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user_entry = User.query.filter_by(username=username).first()

    if user_entry is None:
        return jsonify({ 'error': 'wrong username or password' }), 400
    else:
        auth_entry = Auth.query.filter_by(email=user_entry.email).first()
        if auth_entry.is_correct_password(password):
            return jsonify({    
                'username': user_entry.username, 
                'email': user_entry.email, 
                'joined': user_entry.joined_at 
            })
        else:
            return jsonify({ 'error': 'wrong username or password' }), 400


@app.route("/user_location", methods=["GET"])
def get_user_location():
    # client_ip = request.remote_addr
    client_ip = '178.140.101.10'                        # TODO: get ip automatically
    # request to dadata API
    payload = { 'ip': client_ip }
    headers = {
        "Accept": "application/json",
        "Authorization": f'Token {DADATA_KEY}'
    }
    url = DADATA_URL + 'iplocate/address'
    response = requests.get(url, params=payload, headers=headers)
    location = response.json()['location']
    if location is None:
        return jsonify({ 'error': 'was not able to determine location' }), 400
    else:
        data = location['data']
        return jsonify({
            'lat': data['geo_lat'],
            'lon': data['geo_lon'],
            'city': data['city'],
            'country': data['country'],
            'isoCode': data['region_iso_code'],
        }), 200


@app.route("/suggestions", methods=["POST"])
def get_suggestions():
    headers =  {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Token {DADATA_KEY}'
    }
    payload = {
        "query": request.json['query'],
        "count": request.json['count'],
        "locations": [
            { 
                "city": request.json['city'],
                "country": request.json['country']
            }
        ],
        "restrict_value": True
    }
    url = DADATA_URL + 'suggest/address'
    response = requests.post(url, json=payload, headers=headers)
    suggestions = response.json()['suggestions']
    if not suggestions:
        return jsonify({ 'error': 'no suggestions available' }), 400
    else:
        result = []
        for elem in suggestions:
            suggestion = {
                "lat": elem['data']['geo_lat'],
                "lon": elem['data']['geo_lon'],
                "fiasLevel": elem['data']['fias_level'],
                "fullAddress": elem['unrestricted_value'],
                "address": elem['value']
            }
            result.append(suggestion)

        return jsonify(result), 200


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