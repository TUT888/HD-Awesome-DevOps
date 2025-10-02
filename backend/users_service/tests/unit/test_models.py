"""Unit tests for SQLAlchemy models."""
from app.models import User


def test_user_repr():
    """Test user model string representation."""
    user = User(id=1, username="testuser", email="test@example.com")
    repr_str = repr(user)
    assert "User" in repr_str
    assert "id=1" in repr_str
    assert "testuser" in repr_str