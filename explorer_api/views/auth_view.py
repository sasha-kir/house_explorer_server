from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError

from ..models import db
from ..models.User import User
from ..models.Auth import Auth

from ..shared.Authentication import TokenAuth

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register_user():
    username = request.json.get('username', '')
    email = request.json.get('email', '')
    password = request.json('password', '')
    if not username or not password or not email:
        return jsonify({ "error": "wrong request parameters" }), 400

    new_user = User(username=username, email=email)
    new_auth = Auth(email=email, plaintext_password=password)

    db.session.add(new_user)
    db.session.add(new_auth)

    try:
        db.session.commit()
         # generate token
        token_result = TokenAuth.generate_token(email)
        if 'token' in token_result:
            return jsonify({ 'token': token_result['token'] }), 200
        else:
            return jsonify(token_result), 400
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
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    if not username or not password:
        return jsonify({ "error": "wrong request parameters" }), 400

    user_entry = User.query.filter_by(username=username).first()

    if user_entry is None:
        return jsonify({ 'error': 'wrong username or password' }), 401
    else:
        auth_entry = Auth.query.filter_by(email=user_entry.email).first()
        if auth_entry.is_correct_password(password):
            # generate token
            token_result = TokenAuth.generate_token(user_entry.email)
            if 'token' in token_result:
                return jsonify({ 'token': token_result['token'] }), 200
            else:
                return jsonify(token_result), 400
        else:
            return jsonify({ 'error': 'wrong username or password' }), 401


@auth.route('/check_token', methods=["POST"])
def check_token():
    token = request.json.get('token', '')
    decode_result = TokenAuth.decode_token(token)

    if 'user_email' in decode_result:
        return jsonify({ 'success': True }), 200
    else:
        return jsonify(decode_result), 401

