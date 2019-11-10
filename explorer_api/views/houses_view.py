import os
import requests

from flask import request, jsonify, Blueprint

from explorer_api.utils.house_scraper import scrape_house_info
from explorer_api.utils.type_finder import find_type_link

from ..shared.Authentication import TokenAuth

house_info = Blueprint('dadata', __name__)

DADATA_KEY = os.environ['DADATA_KEY']
DADATA_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/'


@house_info.route("/user_location", methods=["GET"])
def get_user_location():
    client_ip = request.remote_addr
    # request to dadata API
    payload = { 'ip': client_ip }
    headers = {
        "Accept": "application/json",
        "Authorization": f'Token {DADATA_KEY}'
    }
    url = DADATA_URL + 'iplocate/address'
    response = requests.get(url, params=payload, headers=headers)
    location = response.json().get('location', None)
    if location is None:
        return jsonify({ 'error': 'was not able to determine location' }), 500
    else:
        data = location.get('data')
        return jsonify({
            'lat': data['geo_lat'],
            'lon': data['geo_lon'],
            'city': data['city'],
            'country': data['country'],
            'isoCode': data['region_iso_code'],
        }), 200


@house_info.route("/suggestions", methods=["POST"])
def get_suggestions():
    headers =  {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Token {DADATA_KEY}'
    }
    payload = {
        "query": request.json.get('query', ''),
        "count": request.json.get('count', 10),
        "locations": [
            { 
                "city": request.json.get('city', ''),
                "country": request.json.get('country', '')
            }
        ],
        "restrict_value": True
    }
    url = DADATA_URL + 'suggest/address'
    response = requests.post(url, json=payload, headers=headers)
    suggestions = response.json().get('suggestions', '')
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


@house_info.route("/house_info", methods=["POST"])
def get_house_info():
    headers =  {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Token {DADATA_KEY}'
    }
    payload = {
        "query": request.json.get('query', ''),
        "count": 1,
        "locations": [
            { 
                "city": request.json.get('city', ''),
                "country": request.json.get('country', '')
            }
        ],
        "restrict_value": True
    }
    url = DADATA_URL + 'suggest/address'
    response = requests.post(url, json=payload, headers=headers)
    suggestions = response.json().get('suggestions', '')
    if not suggestions:
        return jsonify({ 'error': 'house info not available' }), 400
    else:
        data = suggestions[0]['data']

        fias_level = int(data['fias_level'])
        if data['house']:
            fias_level = 8

        # check if dadata returned house
        if fias_level < 8:
            house_info = {
                "lat": data['geo_lat'],
                "lon": data['geo_lon'],
                "fiasLevel": data['fias_level'],
                "fullAddress": suggestions[0]['unrestricted_value'],
                "address": suggestions[0]['value']
            }
            return jsonify(house_info), 200

        # fetch house info
        scraping_result = scrape_house_info(
            data["city"],
            data["street_type"], 
            data["street"],
            data["house_type"],
            data["house"],
            data["block_type"],
            data["block"]
        )

        if "error" in scraping_result.keys():
            return jsonify({
                "scraping error": scraping_result["error"]
            }), 400

        house_type_link = find_type_link(scraping_result["house_type"])

        house_info = {
            "lat": data['geo_lat'],
            "lon": data['geo_lon'],
            "fiasLevel": fias_level,
            "fullAddress": suggestions[0]['unrestricted_value'],
            "infoBlock": {
                "address": f'{data["city"]}, {suggestions[0]["value"]}',
                "yearBuilt": scraping_result["year_built"],
                "houseType": scraping_result["house_type"],
                "houseTypeLink": house_type_link,
                "floorCount": scraping_result["floor_count"],
                "wallsMaterial": scraping_result["walls_material"],
            }
        }

        return jsonify(house_info), 200
