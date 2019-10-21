from datetime import datetime
from hashlib import md5
from flask import request, jsonify, Blueprint

from ..models.User import User

from ..shared.Authentication import TokenAuth

profile = Blueprint('profile', __name__)


@profile.route('/profile', methods=['POST'])
def get_user_profile():
    token = request.json["token"]
    decode_result = TokenAuth.decode_token(token)
    email = decode_result.get("user_email", "")

    if not email:
        return jsonify({ "error": "invalid token" }), 401

    user_entry = User.query.filter_by(email=email).first()

    if not user_entry:
        return jsonify({ "error": "invalid token" }), 401

    current_date = datetime.now().date()
    dates_delta = current_date - user_entry.joined_at.date()

    email_hash = md5(bytes(email, encoding="utf-8")).hexdigest()
    gravatar_link = 'https://www.gravatar.com/avatar/' + email_hash + "?d=mp&s=200"

    return jsonify({ 
        "userPic": gravatar_link,
        "username": user_entry.username,
        "email": email,
        "daysRegistered": dates_delta.days,
    }), 200


@profile.route('/userpic', methods=['POST'])
def get_userpic():
    token = request.json["token"]
    decode_result = TokenAuth.decode_token(token)
    email = decode_result.get("user_email", "")

    if not email:
        return jsonify({ "error": "invalid token" }), 401

    email_hash = md5(bytes(email, encoding="utf-8")).hexdigest()
    gravatar_link = 'https://www.gravatar.com/avatar/' + email_hash + "?d=mp&s=100"

    return jsonify({
        "userPic": gravatar_link
    }), 200