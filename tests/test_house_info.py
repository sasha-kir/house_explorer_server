import pytest

def test_valid_address(test_client):
    query = "Москва, Нагатинский бульвар 6"
    response = test_client.post('/house_info',
                                json={
                                    'query': query,
                                    'city': 'Москва',
                                    'country': 'Россия'
                                })

    assert response.status_code == 200

    house_info_keys = ["lat", "lon", "fiasLevel", "fullAddress", "infoBlock"]

    assert all(key in response.json.keys() for key in house_info_keys)


def test_invalid_address(test_client):
    query = "фывапролджэ"
    response = test_client.post('/house_info',
                                json={
                                    'query': query,
                                    'city': 'Москва',
                                    'country': 'Россия'
                                })

    assert response.status_code == 400
    assert response.json['error'] == 'house info not available'


def test_non_house_address(test_client):
    query = "Москва, Нагатинский бульвар"
    response = test_client.post('/house_info',
                                json={
                                    'query': query,
                                    'city': 'Москва',
                                    'country': 'Россия'
                                })

    assert response.status_code == 200
    house_info_keys = ["lat", "lon", "fiasLevel", "fullAddress", "address"]
    assert all(key in response.json.keys() for key in house_info_keys)


def test_address_not_in_mingkh(test_client):
    query = "Санкт-Петербург, Школьная, 100"
    response = test_client.post('/house_info',
                                json={
                                    'query': query, 
                                    'city': 'Санкт-Петербург',
                                    'country': 'Россия'
                                })

    assert response.status_code == 400
    assert "scraping error" in response.json.keys()