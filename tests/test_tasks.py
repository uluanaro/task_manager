def test_create_task(client, auth_headers):
    response = client.post("/api/v1/tasks/", json={
        "title": "Тестовая задача",
        "description": "Описание",
        "priority": "high"
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовая задача"
    assert data["priority"] == "high"
    assert data["is_completed"] == False


def test_get_tasks(client, auth_headers):
    client.post("/api/v1/tasks/", json={"title": "Задача 1"}, headers=auth_headers)
    client.post("/api/v1/tasks/", json={"title": "Задача 2"}, headers=auth_headers)

    response = client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_tasks_unauthorized(client):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 401


def test_get_task_by_id(client, auth_headers):
    created = client.post("/api/v1/tasks/", json={
        "title": "Моя задача"
    }, headers=auth_headers).json()

    response = client.get(f"/api/v1/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Моя задача"


def test_update_task(client, auth_headers):
    created = client.post("/api/v1/tasks/", json={
        "title": "Старый заголовок"
    }, headers=auth_headers).json()

    response = client.patch(f"/api/v1/tasks/{created['id']}", json={
        "title": "Новый заголовок",
        "is_completed": True
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Новый заголовок"
    assert response.json()["is_completed"] == True


def test_delete_task(client, auth_headers):
    created = client.post("/api/v1/tasks/", json={
        "title": "Удалить меня"
    }, headers=auth_headers).json()

    response = client.delete(f"/api/v1/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/api/v1/tasks/{created['id']}", headers=auth_headers)
    assert response.status_code == 404


def test_user_sees_only_own_tasks(client):
    client.post("/api/v1/auth/register", json={"email": "user1@test.com", "password": "123456"})
    client.post("/api/v1/auth/register", json={"email": "user2@test.com", "password": "123456"})

    token1 = client.post("/api/v1/auth/login", data={
        "username": "user1@test.com", "password": "123456"
    }).json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    token2 = client.post("/api/v1/auth/login", data={
        "username": "user2@test.com", "password": "123456"
    }).json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}


    client.post("/api/v1/tasks/", json={"title": "Задача user1"}, headers=headers1)

    response = client.get("/api/v1/tasks/", headers=headers2)
    assert len(response.json()) == 0

def test_filter_by_completed(client, auth_headers):
    task1 = client.post("/api/v1/tasks/", json={
        "title": "Задача 1"
    }, headers=auth_headers).json()
    task2 = client.post("/api/v1/tasks/", json={
        "title": "Задача 2"
    }, headers=auth_headers).json()

    client.patch(f"/api/v1/tasks/{task1['id']}", json={
        "is_completed": True
    }, headers=auth_headers)

    completed = client.get("/api/v1/tasks/?is_completed=true", headers=auth_headers).json()
    assert len(completed) == 1
    assert completed[0]["title"] == "Задача 1"

    active = client.get("/api/v1/tasks/?is_completed=false", headers=auth_headers).json()
    assert len(active) == 1
    assert active[0]["title"] == "Задача 2"
