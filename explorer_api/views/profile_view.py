from datetime import datetime
from hashlib import md5
from flask import request, jsonify, Blueprint

from ..shared.Authentication import TokenAuth

profile = Blueprint("profile", __name__)


@profile.route("/profile", methods=["POST"])
def get_user_profile():
    token = request.json.get("token", "")
    decode_result = TokenAuth.user_from_token(token)

    if "error" in decode_result:
        return jsonify({"error": "invalid token"}), 401

    user_entry = decode_result["success"]

    current_date = datetime.now().date()
    dates_delta = current_date - user_entry.joined_at.date()

    email_hash = md5(bytes(user_entry.email, encoding="utf-8")).hexdigest()
    gravatar_link = "https://www.gravatar.com/avatar/" + email_hash + "?d=mp&s=200"

    return (
        jsonify(
            {
                "userPic": gravatar_link,
                "username": user_entry.username,
                "email": user_entry.email,
                "daysRegistered": dates_delta.days,
            }
        ),
        200,
    )


@profile.route("/userpic", methods=["POST"])
def get_userpic():
    token = request.json.get("token", "")
    decode_result = TokenAuth.decode_token(token)
    email = decode_result.get("user_email", "")

    if not email:
        return jsonify({"error": "invalid token"}), 401

    email_hash = md5(bytes(email, encoding="utf-8")).hexdigest()
    gravatar_link = "https://www.gravatar.com/avatar/" + email_hash + "?d=mp&s=100"

    return jsonify({"userPic": gravatar_link}), 200
