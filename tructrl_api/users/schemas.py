"""
File:         schemas.py
Module:       users
Project:      TruCtrl-API
Copyrigh:     © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:      MIT
Description:  Pydantic schemas for user management in the TruCtrl-API application.
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
    is_active: bool
    is_superuser: bool

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
