"""SQLAlchemy models."""
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from .db import Base


class User(Base):  # pylint: disable=too-few-public-methods
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # pylint: disable=not-callable
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"