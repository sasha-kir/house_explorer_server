def test_valid_query(test_client):
    query = "колом"
    count = 5
    response = test_client.post(
        "/suggestions",
        json={"query": query, "count": count, "city": "Москва", "country": "Россия"},
    )

    assert response.status_code == 200
    assert len(response.json) == count

    suggestion_keys = ["lat", "lon", "fiasLevel", "fullAddress", "address"]

    for suggestion in response.json:
        assert all(key in suggestion.keys() for key in suggestion_keys)


def test_invalid_query(test_client):
    query = "abcdefgh"
    count = 5
    response = test_client.post(
        "/suggestions",
        json={"query": query, "count": count, "city": "Москва", "country": "Россия"},
    )

    assert response.status_code == 400
    assert response.json["error"] == "no suggestions available"
