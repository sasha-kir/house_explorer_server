from datetime import datetime

from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError

from ..models import db
from ..models.User import User

from ..shared.Authentication import TokenAuth

profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['POST'])
def get_user_profile():
    token = request.json["token"]
    decode_result = TokenAuth.decode_token(token)
    email = decode_result.get("user_email", "")

    if not email:
        return jsonify({ "error": "invalid token" }), 400

    user_entry = User.query.filter_by(email=email).first()

    if not user_entry:
        return jsonify({ "error": "invalid token" }), 400

    current_date = datetime.now().date()
    dates_delta = current_date - user_entry.joined_at.date()

    return jsonify({ 
        "username": user_entry.username,
        "email": email,
        "daysRegistered": dates_delta.days,
    }), 200