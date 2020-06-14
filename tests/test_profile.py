from explorer_api.shared.Authentication import TokenAuth


def test_valid_profile(test_client, init_database):
    username = "test"
    email = "test@test.com"

    token = TokenAuth.generate_token(email)["token"]

    response = test_client.post("/profile", json={"token": token,})

    assert response.status_code == 200

    profile_keys = ["username", "email", "daysRegistered", "userPic"]
    assert all(key in response.json.keys() for key in profile_keys)

    assert response.json["username"] == username
    assert response.json["email"] == email


def test_invalid_token_on_profile(test_client, init_database):
    email = "example@test.com"

    token = TokenAuth.generate_token(email)["token"]

    response = test_client.post("/profile", json={"token": token,})

    assert response.status_code == 401
    assert response.json["error"] == "invalid token"
