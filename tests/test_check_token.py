import pytest
import os
import jwt
from datetime import datetime, timedelta

from explorer_api.shared.Authentication import TokenAuth

def test_valid_token(test_client):
    
    email = "test@test.com"

    token = TokenAuth.generate_token(email)['token']

    response = test_client.post('/check_token',
                                json={
                                    'token': token,
                                })

    assert response.status_code == 200


def test_invalid_token(test_client):

    token = "abcdef"

    response = test_client.post('/check_token',
                                json={
                                    'token': token,
                                })

    assert response.status_code == 401
    assert response.json['error'] == 'invalid token'


def test_expired_token(test_client):

    token = jwt.encode(
                {
                    'exp': datetime.utcnow() + timedelta(-30),
                    'sub': 'test@test.com'
                },
                os.environ['JWT_KEY'],
                algorithm='HS256'
            ).decode("utf-8")
    
    response = test_client.post('/check_token',
                                json={
                                    'token': token,
                                })

    assert response.status_code == 401
    assert response.json['error'] == 'token expired, please login again'    
