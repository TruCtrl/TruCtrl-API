"""
File:           schemas.py
Module:         users
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    Schema Layer for User Management.
                Defines Pydantic models for data validation, serialization, and deserialization.
                Used for request and response bodies in API endpoints.
                Keeps API contracts separate from database models.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
