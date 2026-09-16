def test_unauthorized_user_cannot_get_tasks(anonymous_client):
    response = anonymous_client.get("/Todo/Tasks")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_authorized_user_can_get_tasks(authorized_client):
    response = authorized_client.get("/Todo/Tasks")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_authorized_user_can_create_task(authorized_client):
    # create a task
    payload = {
        "title": "test task",
        "description": "test description",
        "is_completed": False,
    }
    response = authorized_client.post("/Todo/Tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "test task"
    assert response.json()["description"] == "test description"
    assert response.json()["is_completed"] == False
