from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError

from ..models import db
from ..models.User import User
from ..models.Auth import Auth

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
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


@auth.route('/login', methods=['POST'])
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