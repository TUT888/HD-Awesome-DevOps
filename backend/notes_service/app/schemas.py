"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class NoteBase(BaseModel):
    """Base note schema with common fields."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    user_id: int = Field(..., gt=0)


class NoteCreate(NoteBase):
    """Schema for creating a new note."""

    pass


class NoteUpdate(BaseModel):
    """Schema for updating an existing note."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)


class NoteResponse(NoteBase):
    """Schema for note response."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
