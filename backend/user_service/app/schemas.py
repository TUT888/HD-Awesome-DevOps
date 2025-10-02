"""Pydantic schemas."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating user."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    email: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)