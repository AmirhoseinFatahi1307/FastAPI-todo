def test_login_invalid_credentials(anonymous_client):
    # username correct but password incorrect
    payload = {"username": "user_test", "password": "12345678"}
    response = anonymous_client.post("/users/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

    # username incorrect but password correct
    payload = {"username": "user", "password": "1234"}
    response = anonymous_client.post("/users/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_response_200(anonymous_client):
    payload = {"username": "user_test", "password": "1234"}
    response = anonymous_client.post("/users/login", json=payload)
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


def test_register_response_201(anonymous_client):
    payload = {
        "username": "amir1234",
        "password": "amir1234",
        "password_confirm": "amir1234",
    }
    response = anonymous_client.post("/users/register", json=payload)
    assert response.status_code == 201
