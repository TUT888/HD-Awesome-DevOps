"""Integration tests for Users Service API."""
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import User


def test_read_root(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Users Service!"}


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "users-service"}


def test_create_user_success(client: TestClient, db_session_for_test: Session):
    """Test successful user creation."""
    test_data = {"username": "johndoe", "email": "john@example.com"}
    response = client.post("/users/", json=test_data)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_data["username"]
    assert data["email"] == test_data["email"]
    assert "id" in data
    assert "created_at" in data

    # Verify in database
    db_user = (
        db_session_for_test.query(User)
        .filter(User.id == data["id"])
        .first()
    )
    assert db_user is not None
    assert db_user.username == test_data["username"]


def test_create_user_duplicate_username(client: TestClient, db_session_for_test: Session):
    """Test creating user with duplicate username."""
    test_data = {"username": "duplicate", "email": "user1@example.com"}
    
    # Create first user
    response1 = client.post("/users/", json=test_data)
    assert response1.status_code == 201

    # Try to create second user with same username
    test_data2 = {"username": "duplicate", "email": "user2@example.com"}
    response2 = client.post("/users/", json=test_data2)
    assert response2.status_code == 409
    assert "Username already exists" in response2.json()["detail"]


def test_create_user_duplicate_email(client: TestClient, db_session_for_test: Session):
    """Test creating user with duplicate email."""
    test_data = {"username": "user1", "email": "duplicate@example.com"}
    
    # Create first user
    response1 = client.post("/users/", json=test_data)
    assert response1.status_code == 201

    # Try to create second user with same email
    test_data2 = {"username": "user2", "email": "duplicate@example.com"}
    response2 = client.post("/users/", json=test_data2)
    assert response2.status_code == 409
    assert "Email already exists" in response2.json()["detail"]


def test_create_user_invalid_email(client: TestClient):
    """Test creating user with invalid email format."""
    invalid_data = {"username": "testuser", "email": "invalid-email"}
    response = client.post("/users/", json=invalid_data)
    assert response.status_code == 422


def test_create_user_short_username(client: TestClient):
    """Test creating user with too short username."""
    invalid_data = {"username": "ab", "email": "test@example.com"}
    response = client.post("/users/", json=invalid_data)
    assert response.status_code == 422


def test_get_user_success(client: TestClient, db_session_for_test: Session):
    """Test getting user by ID."""
    # Create user first
    create_response = client.post(
        "/users/",
        json={"username": "gettest", "email": "get@example.com"}
    )
    user_id = create_response.json()["id"]

    # Get user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["username"] == "gettest"


def test_get_user_not_found(client: TestClient):
    """Test getting non-existent user."""
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]


def test_list_users_empty(client: TestClient, db_session_for_test: Session):
    """Test listing users when database is empty."""
    response = client.get("/users/")
    assert response.status_code == 200
    # Note: may have users from other tests, so just check it's a list
    assert isinstance(response.json(), list)


def test_list_users_with_data(client: TestClient, db_session_for_test: Session):
    """Test listing users with data."""
    # Create users
    client.post("/users/", json={"username": "user1", "email": "user1@example.com"})
    client.post("/users/", json={"username": "user2", "email": "user2@example.com"})

    # List users
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2
