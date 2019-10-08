import pytest

from explorer_api.shared.Authentication import TokenAuth

def test_valid_login(test_client, init_database):
    username = 'test'
    email = 'test@test.com'
    password = 'secret'

    response = test_client.post('/login',
                                json={
                                    'username': username, 
                                    'password': password
                                })
    assert response.status_code == 200
    assert "token" in response.json

    token = response.json["token"]
    decoded_result = TokenAuth.decode_token(token)

    assert "user_email" in decoded_result
    assert decoded_result["user_email"] == email


def test_invalid_login(test_client, init_database):
    correct_username = 'test'
    correct_password = 'secret'

    fake_username = 'fake_user'
    fake_password = 'fake_password'

    response = test_client.post('/login',
                                json={
                                    'username': correct_username, 
                                    'password': fake_password
                                })
    assert response.status_code == 401
    assert response.json['error'] == "wrong username or password"

    response = test_client.post('/login',
                                json={
                                    'username': fake_username, 
                                    'password': correct_password
                                })
    assert response.status_code == 401
    assert response.json['error'] == "wrong username or password"

    response = test_client.post('/login',
                                json={
                                    'username': fake_username, 
                                    'password': fake_password
                                })
    assert response.status_code == 401
    assert response.json['error'] == "wrong username or password"
