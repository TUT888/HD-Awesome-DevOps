"""SQLAlchemy database models."""

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from .db import Base


class Note(Base):
    """Note model for storing user notes."""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}', user_id={self.user_id})>"
