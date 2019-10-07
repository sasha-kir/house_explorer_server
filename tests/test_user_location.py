import pytest

def test_user_location(test_client):

    response = test_client.get('/user_location')

    assert response.status_code == 200

    response_keys = ["lat", "lon", "city", "country", "isoCode"]
    
    assert all(key in response.json for key in response_keys)