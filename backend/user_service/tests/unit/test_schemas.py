"""Unit tests for Pydantic schemas."""
import pytest
from pydantic import ValidationError
from app.schemas import UserCreate


def test_user_create_valid():
    """Test valid user creation schema."""
    user = UserCreate(username="testuser", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_user_create_invalid_email():
    """Test user creation with invalid email."""
    with pytest.raises(ValidationError):
        UserCreate(username="testuser", email="invalid-email")


def test_user_create_short_username():
    """Test user creation with username too short."""
    with pytest.raises(ValidationError):
        UserCreate(username="ab", email="test@example.com")


def test_user_create_long_username():
    """Test user creation with username too long."""
    with pytest.raises(ValidationError):
        UserCreate(username="a" * 51, email="test@example.com")


def test_user_create_empty_username():
    """Test user creation with empty username."""
    with pytest.raises(ValidationError):
        UserCreate(username="", email="test@example.com")