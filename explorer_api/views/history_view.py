import os
import requests

from flask import request, jsonify, Blueprint

from ..models import db
from ..models.User import User
from ..models.History import History

from ..shared.Authentication import TokenAuth

history = Blueprint('history', __name__)


@history.route("/save_house", methods=["POST"])
def save_to_history():
    token = request.json.get('token', '')
    decode_result = TokenAuth.user_from_token(token)

    if "error" in decode_result:
        return jsonify({ "error": "invalid token" }), 401
    
    user_entry = decode_result["success"]

    user_id = user_entry.id
    house_info = request.json.get('houseInfo', '')
    map_coords = request.json.get('mapCoords', '')
    if not house_info or not map_coords:
        return jsonify({ "error": "wrong request parameters" }), 400

    house_coords = f'{map_coords[1]},{map_coords[0]}'

    history_entry = History(
        user_id=user_id, 
        house_info=house_info, 
        house_coords=house_coords
    )
    db.session.add(history_entry)
    db.session.commit()

    return jsonify("house successfully saved"), 200


@history.route("/history", methods=["POST"])
def get_history():
    token = request.json.get('token', '')
    decode_result = TokenAuth.user_from_token(token)

    if "error" in decode_result:
        return jsonify({ "error": "invalid token" }), 401
    
    user_entry = decode_result["success"]

    user_id = user_entry.id
    history_entries = History.query.filter_by(user_id=user_id)

    if history_entries.count() == 0:
        return jsonify({ "history": None }), 200

    result = []
    for row in history_entries:
        result.append({
            "date": row.added_at, 
            "houseInfo": row.house_info,
            "houseCoords": row.house_coords
        })
    return jsonify({ "history": result }), 200


@history.route("/delete_house", methods=["POST"])
def delete_from_history():
    token = request.json.get('token', '')
    decode_result = TokenAuth.user_from_token(token)

    if "error" in decode_result:
        return jsonify({ "error": "invalid token" }), 401
    
    user_entry = decode_result["success"]

    user_id = user_entry.id
    house_coords = request.json.get('houseCoords', '')

    if not house_coords:
        return jsonify({ "error": "wrong request parameters" }), 400

    History.query.filter_by(user_id=user_id, house_coords=house_coords).delete()
    db.session.commit()

    return jsonify("house successfully deleted"), 200

