import os
import requests

from flask import request, jsonify, Blueprint

dadata = Blueprint('dadata', __name__)

DADATA_KEY = os.environ['DADATA_KEY']
DADATA_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/'

@dadata.route("/user_location", methods=["GET"])
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


@dadata.route("/suggestions", methods=["POST"])
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




