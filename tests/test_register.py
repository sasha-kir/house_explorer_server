import pytest

def test_registration(test_client, init_database):
    username = "bob"
    email = "bob@gmail.com"
    password = "12345"

    response = test_client.post('/register',
                                json={
                                    'username': username,
                                    'email': email,
                                    'password': password
                                })

    assert response.status_code == 200
    assert response.json['username'] == username
    assert response.json['email'] == email


def test_existing_username(test_client, init_database):
    username = "test"
    email = "example@example.com"
    password = "1234"

    response = test_client.post('/register',
                                json={
                                    'username': username,
                                    'email': email,
                                    'password': password
                                })

    assert response.status_code == 400
    assert response.json['error'] == 'username already exists'


def test_existing_email(test_client, init_database):
    username = "example"
    email = "test@test.com"
    password = "1234"

    response = test_client.post('/register',
                                json={
                                    'username': username,
                                    'email': email,
                                    'password': password
                                })

    assert response.status_code == 400
    assert response.json['error'] == 'email already exists'



