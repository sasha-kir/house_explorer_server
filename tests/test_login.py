import pytest

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

    assert response.json['username'] == username
    assert response.json['email'] == email


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
    assert response.status_code == 400
    assert response.json['error'] == "wrong username or password"

    response = test_client.post('/login',
                                json={
                                    'username': fake_username, 
                                    'password': correct_password
                                })
    assert response.status_code == 400
    assert response.json['error'] == "wrong username or password"

    response = test_client.post('/login',
                                json={
                                    'username': fake_username, 
                                    'password': fake_password
                                })
    assert response.status_code == 400
    assert response.json['error'] == "wrong username or password"
