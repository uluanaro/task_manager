def test_register_success(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "new@test.com",
        "password": "123456"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@test.com"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client, registered_user):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@test.com",
        "password": "654321"
    })
    assert response.status_code == 400
    assert "уже зарегистрирован" in response.json()["detail"]


def test_login_success(client, registered_user):
    response = client.post("/api/v1/auth/login", data={
        "username": "test@test.com",
        "password": "123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    response = client.post("/api/v1/auth/login", data={
        "username": "test@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401