from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Notes Service!"}


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "notes-service"}


def test_create_note_success(client: TestClient, db_session_for_test: Session):
    test_data = {"title": "Test Note", "content": "Test content", "user_id": 1}
    response = client.post("/notes/", json=test_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == test_data["title"]
    assert data["content"] == test_data["content"]
    assert data["user_id"] == test_data["user_id"]
    assert "id" in data
    assert "created_at" in data


def test_create_note_invalid_user_id(client: TestClient):
    invalid_data = {
        "title": "Invalid Note",
        "content": "Content",
        "user_id": -1,
    }  # Invalid user_id
    response = client.post("/notes/", json=invalid_data)
    assert response.status_code == 422


def test_list_notes_empty(client: TestClient):
    response = client.get("/notes/?user_id=999")
    assert response.status_code == 200
    assert response.json() == []


def test_list_notes_with_data(client: TestClient, db_session_for_test: Session):
    # Create note
    note_data = {"title": "List Test", "content": "Content", "user_id": 1}
    client.post("/notes/", json=note_data)

    # List notes
    response = client.get("/notes/?user_id=1")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert any(n["title"] == "List Test" for n in response.json())


def test_get_note_success(client: TestClient, db_session_for_test: Session):
    # Create note
    create_response = client.post(
        "/notes/", json={"title": "Get Test", "content": "Content", "user_id": 1}
    )
    note_id = create_response.json()["id"]

    # Get note
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id


def test_get_note_not_found(client: TestClient):
    response = client.get("/notes/99999")
    assert response.status_code == 404


def test_update_note_partial(client: TestClient, db_session_for_test: Session):
    # Create note
    create_resp = client.post(
        "/notes/",
        json={"title": "Original", "content": "Original content", "user_id": 1},
    )
    note_id = create_resp.json()["id"]

    # Update
    update_data = {"title": "Updated Title"}
    response = client.put(f"/notes/{note_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_delete_note_success(client: TestClient, db_session_for_test: Session):
    # Create note
    create_resp = client.post(
        "/notes/", json={"title": "Delete Me", "content": "Content", "user_id": 1}
    )
    note_id = create_resp.json()["id"]

    # Delete
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404
